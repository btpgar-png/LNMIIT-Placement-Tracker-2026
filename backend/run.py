import uvicorn
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db

def run_seed():
    from app.seed import seed_database
    try:
        seed_database()
    except Exception as e:
        print(f"Seed error: {e}")
        # Don't fail - the app can still run

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Run seed (don't fail if it errors)
    run_seed()
    
    # Run the application (use import string for reload support)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

