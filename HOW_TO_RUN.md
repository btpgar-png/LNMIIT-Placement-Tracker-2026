# How to Run Placement Tracker

## ⚠️ Important: Batch files don't work in PowerShell!

If you're in PowerShell (which you are), use these methods:

## Method 1: Run PowerShell Scripts (Easiest!)

I'll create PowerShell scripts for you to use instead.

## Method 2: Use CMD Instead

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to project folder:
   ```cmd
   cd C:\Users\jaina\Desktop\Placement-Tracker
   ```
4. Run: `start_backend.bat`

## Method 3: Manual Steps (PowerShell or CMD)

Follow these commands in your current terminal:

### Step 1: Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Step 2: Frontend (in a NEW terminal)

```powershell
cd C:\Users\jaina\Desktop\Placement-Tracker\frontend
npm install
npm start
```




