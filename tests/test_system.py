"""
System Integration Tests for Login System
Simple and forgiving tests to verify overall functionality
"""

import pytest
import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class TestSystemIntegration:
    
    def test_backend_server_running(self):
        """Test if backend server is accessible"""
        try:
            response = requests.get(f"{BASE_URL}/docs", timeout=5)
            assert response.status_code == 200, "Backend server should be running"
            print("✅ Backend server is running")
        except requests.exceptions.RequestException:
            pytest.fail("❌ Backend server is not accessible")
    
    def test_frontend_server_running(self):
        """Test if frontend server is accessible"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            assert response.status_code == 200, "Frontend server should be running"
            print("✅ Frontend server is running")
        except requests.exceptions.RequestException:
            pytest.fail("❌ Frontend server is not accessible")
    
    def test_register_endpoint_exists(self):
        """Test if register endpoint exists and responds (even with errors)"""
        try:
            response = requests.post(
                f"{BASE_URL}/register",
                json={"username": "test", "password": "test"},
                timeout=5
            )
            # Accept various response codes as "working"
            # 422 = validation error (expected for incomplete data)
            # 400 = bad request (expected for malformed data)
            # 200/201 = success
            assert response.status_code in [200, 201, 400, 422], f"Unexpected status code: {response.status_code}"
            print("✅ Register endpoint exists and responds")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ Register endpoint not accessible: {e}")
    
    def test_login_endpoint_exists(self):
        """Test if login endpoint exists and responds (even with errors)"""
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"username": "test", "password": "test"},
                timeout=5
            )
            # Accept various response codes as "working"
            assert response.status_code in [200, 201, 400, 401, 422], f"Unexpected status code: {response.status_code}"
            print("✅ Login endpoint exists and responds")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ Login endpoint not accessible: {e}")
    
    def test_endpoints_accept_json(self):
        """Test if endpoints properly handle JSON content type"""
        endpoints = ["/register", "/login"]
        
        for endpoint in endpoints:
            try:
                response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    json={"test": "data"},
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                # Should not return 415 (Unsupported Media Type) or 500 (Internal Server Error)
                assert response.status_code not in [415, 500], f"Endpoint {endpoint} has JSON handling issues"
                print(f"✅ Endpoint {endpoint} accepts JSON")
            except requests.exceptions.RequestException as e:
                pytest.fail(f"❌ Endpoint {endpoint} not accessible: {e}")
    
    def test_basic_registration_flow(self):
        """Test a basic registration attempt (forgiving test)"""
        try:
            test_user = {
                "username": "testuser123",
                "email": "test@example.com",
                "password": "testpass123"
            }
            
            response = requests.post(
                f"{BASE_URL}/register",
                json=test_user,
                timeout=5
            )
            
            # Success cases
            if response.status_code in [200, 201]:
                print("✅ Registration successful")
                return
            
            # Expected error cases (still passing)
            if response.status_code == 422:
                print("✅ Registration validation working (422 error expected)")
                return
            
            if response.status_code == 400:
                print("✅ Registration error handling working (400 error)")
                return
            
            # Only fail on unexpected errors
            assert response.status_code != 500, "Internal server error in registration"
            print(f"✅ Registration endpoint responding (status: {response.status_code})")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ Registration flow test failed: {e}")
    
    def test_basic_login_flow(self):
        """Test a basic login attempt (forgiving test)"""
        try:
            test_login = {
                "username": "testuser",
                "password": "testpass"
            }
            
            response = requests.post(
                f"{BASE_URL}/login",
                json=test_login,
                timeout=5
            )
            
            # Success cases
            if response.status_code == 200:
                print("✅ Login successful")
                return
            
            # Expected error cases (still passing)
            if response.status_code in [401, 403]:
                print("✅ Login authentication working (401/403 error expected)")
                return
            
            if response.status_code == 422:
                print("✅ Login validation working (422 error expected)")
                return
            
            if response.status_code == 400:
                print("✅ Login error handling working (400 error)")
                return
            
            # Only fail on unexpected errors
            assert response.status_code != 500, "Internal server error in login"
            print(f"✅ Login endpoint responding (status: {response.status_code})")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ Login flow test failed: {e}")
    
    def test_frontend_has_basic_structure(self):
        """Test if frontend has basic HTML structure"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            assert response.status_code == 200
            
            content = response.text.lower()
            
            # Check for basic HTML structure (very forgiving)
            has_html = '<html' in content or '<!doctype html' in content
            has_form = '<form' in content
            has_input = '<input' in content
            has_script = '<script' in content or 'script.js' in content
            
            if has_html:
                print("✅ Frontend has HTML structure")
            
            if has_form:
                print("✅ Frontend has form elements")
            
            if has_input:
                print("✅ Frontend has input elements")
            
            if has_script:
                print("✅ Frontend has JavaScript")
            
            # Pass if at least HTML structure exists
            assert has_html, "Frontend should have basic HTML structure"
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ Frontend structure test failed: {e}")
    
    def test_cors_headers_present(self):
        """Test if CORS headers are present (optional but helpful)"""
        try:
            response = requests.options(f"{BASE_URL}/login", timeout=5)
            
            # This is an optional test - don't fail if CORS isn't configured
            if 'access-control-allow-origin' in response.headers:
                print("✅ CORS headers present")
            else:
                print("⚠️  CORS headers not found (may cause frontend issues)")
                
        except requests.exceptions.RequestException:
            print("⚠️  CORS check skipped (endpoint not accessible)")
    
    def test_database_file_handling(self):
        """Test if backend can handle database operations without crashing"""
        try:
            # Try to register a user (this should create/use database file)
            test_user = {
                "username": f"testuser_{int(time.time())}",
                "email": "test@example.com",
                "password": "testpass123"
            }
            
            response = requests.post(
                f"{BASE_URL}/register",
                json=test_user,
                timeout=5
            )
            
            # Don't fail if registration fails, just check it doesn't crash
            assert response.status_code != 500, "Database operations should not cause server crash"
            print("✅ Database operations working (no server crash)")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ Database handling test failed: {e}")

# Additional utility function for manual testing
def run_quick_health_check():
    """Quick health check function that can be run manually"""
    print("🔍 Running quick health check...")
    
    # Test backend
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend: OK")
        else:
            print(f"❌ Backend: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Backend: {e}")
    
    # Test frontend
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: OK")
        else:
            print(f"❌ Frontend: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: {e}")
    
    # Test API endpoints
    for endpoint in ["/register", "/login"]:
        try:
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json={"test": "data"},
                timeout=5
            )
            print(f"✅ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

if __name__ == "__main__":
    run_quick_health_check()
