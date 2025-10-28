from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company, Base
from datetime import datetime

# Database connection
DATABASE_URL = "sqlite:///./placement_tracker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    try:
        # Delete existing data
        db.query(Company).delete()
        
        # Sample data with dates as date objects
        companies_to_add = [
            {
                "notification_date": datetime(2025, 9, 29).date(),
                "company_name": "Celebal Technologies",
                "type_of_offer": "SLI + FTE",
                "branches_allowed": "CSE, ECE, CCE, Mech",
                "eligibility_cgpa": "5",
                "job_roles": "Data Science, Data Engineer",
                "ctc_stipend": "CTC: ₹7,00,000\nStipend: ₹15,000\nFixed - 600000",
                "students_selected": 8
            },
            {
                "notification_date": datetime(2025, 9, 29).date(),
                "company_name": "FreeCharge",
                "type_of_offer": "SLI + FTE",
                "branches_allowed": "N/A",
                "eligibility_cgpa": "6",
                "job_roles": "Devops, Data engineer, Quality Assurance, Frontend Developer, Backend Developer(Java)",
                "ctc_stipend": "CTC: ₹7,00,000\nStipend: ₹25,000\nFixed - 700000",
                "students_selected": 0
            },
            {
                "notification_date": datetime(2025, 9, 25).date(),
                "company_name": "Provakil",
                "type_of_offer": "SLI + FTE",
                "branches_allowed": "CSE, ECE, CCE, Mech",
                "eligibility_cgpa": "5",
                "job_roles": "Associate Software Developer",
                "ctc_stipend": "CTC: ₹6,50,000\nStipend: ₹20,000\nFixed - 650000",
                "students_selected": 2
            },
        ]
        
        # Add companies
        for data in companies_to_add:
            company = Company(**data)
            db.add(company)
        
        db.commit()
        print(f"✓ Successfully added {len(companies_to_add)} companies!")
        return True
        
    except Exception as e:
        print(f"✗ Error seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

