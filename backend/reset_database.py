import os
import sys

# Delete existing database
db_path = "placement_tracker.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✓ Deleted {db_path}")

# Run seed
from app.seed import seed_database
print("Seeding database with 31 companies...")
seed_database()
print("\n✓ Database reset complete!")
print("Now run: python run.py")

