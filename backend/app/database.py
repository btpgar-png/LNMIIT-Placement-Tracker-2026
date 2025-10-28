from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for easier setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./placement_tracker.db")

# Create engine with appropriate connection args
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
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

