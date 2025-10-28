"""Run this to fix the database"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.models import Company, Base
from app.database import engine, SessionLocal

# Delete existing database
if os.path.exists("placement_tracker.db"):
    os.remove("placement_tracker.db")
    print("✓ Old database deleted")

# Create tables
Base.metadata.create_all(bind=engine)
print("✓ Database created")

# Create database session
db = SessionLocal()

# Sample companies with PROPER date objects
companies = [
    Company(
        notification_date=datetime(2025, 9, 29).date(),
        company_name="Celebal Technologies",
        type_of_offer="SLI + FTE",
        branches_allowed="CSE, ECE, CCE, Mech",
        eligibility_cgpa="5",
        job_roles="Data Science, Data Engineer",
        ctc_stipend="CTC: ₹7,00,000\nStipend: ₹15,000\nFixed - 600000",
        students_selected=8
    ),
    Company(
        notification_date=datetime(2025, 9, 29).date(),
        company_name="FreeCharge",
        type_of_offer="SLI + FTE",
        branches_allowed="N/A",
        eligibility_cgpa="6",
        job_roles="Devops, Data engineer, Quality Assurance, Frontend Developer, Backend Developer(Java)",
        ctc_stipend="CTC: ₹7,00,000\nStipend: ₹25,000\nFixed - 700000",
        students_selected=0
    ),
    Company(
        notification_date=datetime(2025, 9, 25).date(),
        company_name="Provakil",
        type_of_offer="SLI + FTE",
        branches_allowed="CSE, ECE, CCE, Mech",
        eligibility_cgpa="5",
        job_roles="Associate Software Developer",
        ctc_stipend="CTC: ₹6,50,000\nStipend: ₹20,000\nFixed - 650000",
        students_selected=2
    ),
]

# Add to database
for company in companies:
    db.add(company)

db.commit()
print(f"✓ Added {len(companies)} companies to database!")
print("✓ Database fixed! Now run: python run.py")

