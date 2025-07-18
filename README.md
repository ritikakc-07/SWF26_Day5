# Login System Lab

## Overview
This is a full stack system for teaching how a full stack app works on basic and how to PRs in a collaborative workflow.

# Your Task
- Fork the repository.
- Clone the repository.
- Unzip the provided zip.
- Rename the YourName_SomethingYouLike/ folder with your name and what you like. 
- Then, go inside the folder.
- In the backend, complete the task provided in the main.py
- In the frontend, complete the task provided in the index.html and script.js
- Follow the Readme Provided to follow along. 
- Test the working system locally.
- Push the working repository.
- Create a pull request.

## Structure
```
├── .github/workflows/ci-cd.yml    # GitHub Actions CI/CD pipeline
├── YourName_SomethingYouLike/
|   ├── backend/                       # FastAPI backend
|   │   ├── main.py                   # API endpoints
|   │   ├── requirements.txt          # Python dependencies
|   │   └── database.json             # JSON database (created automatically)
|   ├── frontend/                      # HTML/CSS/JS frontend
|   │   ├── index.html               # Main HTML file
|   │   ├── styles.css               # CSS styling
|   │   └── script.js                # JavaScript functionality
├── tests/                        # System integration tests
│   └── test_system.py           # Automated tests
```

## Quick Start


### 1. Start the backend  
- Create a virtual env (use version 3.12 > python > 3.6 ) 
```bash
# Start backend (Terminal 1)
cd backend
python -m venv venv

# FOR LINUX USE
source venv/bin/activate
# FOR WINDOWS USE
./venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --reload
```
- Run Backend API: http://localhost:8000

### 2. Start the frontend
```bash
# Start frontend (Terminal 2)
cd frontend
python -m http.server 3000
```
- Run Frontend API: http://localhost:3000
