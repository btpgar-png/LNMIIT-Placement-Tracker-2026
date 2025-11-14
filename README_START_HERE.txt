═══════════════════════════════════════════════════════════════
     PLACEMENT TRACKER - START HERE! (PowerShell Guide)
═══════════════════════════════════════════════════════════════

✅ STEP-BY-STEP INSTRUCTIONS FOR POWERSHELL:
═══════════════════════════════════════════════════════════════

Open PowerShell in the Placement-Tracker folder and run:

───────────────────────────────────────────────────────────────
STEP 1: Setup Backend (First Time Only)
───────────────────────────────────────────────────────────────

Copy and paste these commands ONE AT A TIME:

cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Wait for installation to complete (may take 2-3 minutes)

───────────────────────────────────────────────────────────────
STEP 2: Start Backend Server
───────────────────────────────────────────────────────────────

Make sure you're still in the backend folder with venv activated,
then run:

python run.py

You should see:
✓ "INFO: Application startup complete"
✓ "Uvicorn running on http://0.0.0.0:8000"

KEEP THIS TERMINAL OPEN!

───────────────────────────────────────────────────────────────
STEP 3: Start Frontend (Open a NEW PowerShell Window)
───────────────────────────────────────────────────────────────

1. Press Win + X
2. Click "Windows PowerShell" or "Terminal"
3. Navigate to frontend:

cd C:\Users\jaina\Desktop\Placement-Tracker\frontend

4. Install dependencies (first time only):

npm install

5. Start frontend:

npm start

6. Browser opens automatically at http://localhost:3000

───────────────────────────────────────────────────────────────

🎉 DONE! Your app is now running!

═══════════════════════════════════════════════════════════════

IMPORTANT NOTES:
═══════════════════════════════════════════════════════════════

✓ Keep BOTH terminals open while using the app
✓ Backend terminal shows API requests
✓ Frontend terminal shows React updates
✓ Don't close terminals or app will stop

NEXT TIME YOU WANT TO RUN:
───────────────────────────────────────────────────────────────
Just run these 2 commands (in separate terminals):
  
Terminal 1:
  cd backend
  .\venv\Scripts\Activate.ps1  
  python run.py

Terminal 2:
  cd frontend
  npm start

═══════════════════════════════════════════════════════════════

TROUBLESHOOTING:
═══════════════════════════════════════════════════════════════

Problem: "cannot be loaded because running scripts is disabled"
Fix: Run this ONCE in PowerShell (as Administrator):
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Problem: "pip is not recognized"
Fix: Install Python from python.org (make sure to check "Add to PATH")

Problem: "npm is not recognized"
Fix: Install Node.js from nodejs.org

Problem: Port 8000 or 3000 already in use
Fix: Close other programs using those ports

═══════════════════════════════════════════════════════════════


