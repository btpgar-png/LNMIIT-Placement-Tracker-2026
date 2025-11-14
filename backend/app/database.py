from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for easier setup
# For production (Render/cloud), use persistent disk storage
# For local development, use backend directory

# Check if we're in a cloud environment (Render, Railway, etc.)
# Render provides /opt/render/project/src as persistent storage
# Also check for other common cloud paths
CLOUD_PATHS = [
    "/opt/render/project/src",  # Render
    "/app",  # Docker/Render default
    "/tmp",  # Fallback (not ideal but works)
]

def get_persistent_storage_path():
    """Get a persistent storage path for the database"""
    # First, check if DATABASE_URL is explicitly set (for PostgreSQL, etc.)
    if os.getenv("DATABASE_URL") and not os.getenv("DATABASE_URL", "").startswith("sqlite"):
        return None  # Using external database
    
    # Check for cloud environment
    for cloud_path in CLOUD_PATHS:
        if os.path.exists(cloud_path):
            # Use a persistent subdirectory
            persistent_dir = Path(cloud_path) / "data"
            persistent_dir.mkdir(exist_ok=True)
            return persistent_dir / "placement_tracker.db"
    
    # Local development: use backend directory
    BACKEND_DIR = Path(__file__).parent.parent
    return BACKEND_DIR / "placement_tracker.db"

# Get database file path
DB_FILE = get_persistent_storage_path()

# Use absolute path to ensure database is always in the same location
# Convert to forward slashes for SQLite (works on both Windows and Unix)
if DB_FILE:
    db_path = str(DB_FILE.absolute()).replace("\\", "/")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
else:
    # Using external database (PostgreSQL, etc.)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./placement_tracker.db")

# Create engine with appropriate connection args
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Ensure database directory exists (important for cloud deployments)
    if DB_FILE and DB_FILE.parent:
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    Base.metadata.create_all(bind=engine)
    # Lightweight migration: add 'process' column if missing
    try:
        with engine.connect() as conn:
            cols = conn.execute(text("PRAGMA table_info(companies)")).fetchall()
            names = {row[1] for row in cols}  # 0: cid, 1: name
            if "process" not in names:
                conn.execute(text("ALTER TABLE companies ADD COLUMN process TEXT NOT NULL DEFAULT 'Completed'"))
                conn.commit()
    except Exception:
        # Do not crash app if pragma/alter fails; table may not exist yet
        pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

