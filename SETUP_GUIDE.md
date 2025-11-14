# Quick Setup Guide

## Step 1: Start the Backend Server

### Option A: Using the Batch File (Easiest)

Double-click `start_backend.bat` and wait for the server to start.

### Option B: Manual Start

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The backend will automatically:

- Create the SQLite database
- Seed it with 31 sample companies from your data
- Start the API server at http://localhost:8000

## Step 2: Start the Frontend

### Option A: Using the Batch File

Double-click `start_frontend.bat`

### Option B: Manual Start

```bash
cd frontend
npm install
npm start
```

The frontend will start at http://localhost:3000

## Troubleshooting

### Issue: "localhost not reachable"

**Solution:** Make sure the backend server is running first!

1. Check if `placement_tracker.db` exists in the backend folder
2. Look at the backend terminal for any error messages
3. The backend should show "Application startup complete" message

### Issue: "Cannot find module react-scripts"

**Solution:** Run `npm install` in the frontend directory

### Issue: Port already in use

**Solution:** Kill the process using that port or change the port

## Verifying Everything Works

1. Backend API should be accessible at: http://localhost:8000/api/companies
2. You should see a JSON response with 31 companies
3. Frontend should load at: http://localhost:3000
4. Statistics should show real calculated values from the data

## Need Help?

- Backend API docs: http://localhost:8000/docs (Swagger UI)
- Check terminal output for error messages
- Verify Node.js and Python are installed

