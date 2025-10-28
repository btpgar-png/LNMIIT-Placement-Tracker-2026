from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Company, Base
from datetime import datetime, date

# Database connection
DATABASE_URL = "sqlite:///./placement_tracker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Sample data
sample_data = [
    {"notification_date": "2025-09-29", "company_name": "Celebal Technologies", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "5", "job_roles": "Data Science, Data Engineer", "ctc_stipend": "CTC: ₹7,00,000\nStipend: ₹15,000\nFixed - 600000", "students_selected": 8},
    {"notification_date": "2025-09-29", "company_name": "FreeCharge", "type_of_offer": "SLI + FTE", "branches_allowed": "N/A", "eligibility_cgpa": "6", "job_roles": "Devops, Data engineer, Quality Assurance, Frontend Developer, Backend Developer(Java)", "ctc_stipend": "CTC: ₹7,00,000\nStipend: ₹25,000\nFixed - 700000", "students_selected": 0},
    {"notification_date": "2025-09-25", "company_name": "Provakil", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "5", "job_roles": "Associate Software Developer", "ctc_stipend": "CTC: ₹6,50,000\nStipend: ₹20,000\nFixed - 650000", "students_selected": 2},
    {"notification_date": "2025-09-24", "company_name": "ShodhAI", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, CCE", "eligibility_cgpa": "5", "job_roles": "ML, Fullstack, SRE", "ctc_stipend": "CTC: ₹12,49,999.99\nFixed - same as CTC", "students_selected": 0},
    {"notification_date": "2025-09-23", "company_name": "Unicommerce", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "5", "job_roles": "Enterprise Onboarding Profile", "ctc_stipend": "CTC: ₹5,50,000\nStipend: ₹25,000\nFixed - 500000", "students_selected": 4},
    {"notification_date": "2025-09-22", "company_name": "Nagarro Software", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "6", "job_roles": "Full Stack Developer", "ctc_stipend": "CTC: ₹7,00,000\nStipend: ₹30,000\nFixed - 700000", "students_selected": 4},
    {"notification_date": "2025-09-22", "company_name": "TITAN.email", "type_of_offer": "SLI + FTE", "branches_allowed": "N/A", "eligibility_cgpa": "7", "job_roles": "SDE", "ctc_stipend": "CTC: ₹25,00,000\nStipend: ₹1,00,000\nFixed - 1800000 Other Variable - 700000", "students_selected": 0},
    {"notification_date": "2025-09-15", "company_name": "Treebo Hotels", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "6.5", "job_roles": "Backend Developer", "ctc_stipend": "CTC: ₹12,50,000\nStipend: ₹25,000\nFixed - 1100000 ESOPS - 150000", "students_selected": 2},
    {"notification_date": "2025-09-15", "company_name": "Treebo Hotels", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "6.5", "job_roles": "SDET", "ctc_stipend": "CTC: ₹9,50,000\nStipend: ₹15,000\nFixed - 850000", "students_selected": 1},
    {"notification_date": "2025-09-15", "company_name": "Treebo Hotels", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "6.5", "job_roles": "SRE", "ctc_stipend": "CTC: ₹7,00,000\nStipend: ₹15,000\nFixed - 600000", "students_selected": 1},
    {"notification_date": "2025-09-09", "company_name": "Spring Financial", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, CCE", "eligibility_cgpa": "6", "job_roles": "Software Engineer Trainee", "ctc_stipend": "CTC: ₹12,00,000\nStipend: ₹25,000\nFixed - 1200000 + other benefits additional", "students_selected": 3},
    {"notification_date": "2025-09-06", "company_name": "APMSE(Eagleview)", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "5, after shortlisting - 7", "job_roles": "SDE", "ctc_stipend": "CTC: ₹12,84,000\nStipend: ₹50,000\nFixed - 1200000 (Remote)", "students_selected": 7},
    {"notification_date": "2025-09-02", "company_name": "ZS Associates", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "7", "job_roles": "Software Developer, Business Analyst, DAA", "ctc_stipend": "CTC: ₹14,15,000", "students_selected": 19},
    {"notification_date": "2025-08-29", "company_name": "DEShaw", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "7", "job_roles": "SDE", "ctc_stipend": "CTC: ₹59,30,000\nStipend: ₹1,50,000\nFixed - 2400000 Variable* INR 4,00,000 Non Cash Benefits INR 5,30,000 Relocation Allowance** INR 2,00,000 Long Term Incentive*** INR 20,00,000 Joining Bonus INR 4,00,000", "students_selected": 3},
    {"notification_date": "2025-08-28", "company_name": "EPAM", "type_of_offer": "SLI + FTE", "branches_allowed": "N/A", "eligibility_cgpa": "6", "job_roles": "Tech Role", "ctc_stipend": "CTC: ₹8,48,000\nStipend: ₹27,500\nFixed - 800000", "students_selected": 3},
    {"notification_date": "2025-08-27", "company_name": "ProcDNA", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "7", "job_roles": "Business Analyst, Data Science", "ctc_stipend": "CTC: ₹16,74,166\nStipend: ₹25,000\nFixed - 786000", "students_selected": 2},
    {"notification_date": "2025-08-22", "company_name": "Media.net", "type_of_offer": "SLI", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "6", "job_roles": "SDE Intern", "ctc_stipend": "Stipend: ₹1,00,000", "students_selected": 1},
    {"notification_date": "2025-08-21", "company_name": "Triology", "type_of_offer": "FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "N/A", "job_roles": "SDE", "ctc_stipend": "CTC: ₹32,50,000\nFixed - 3000000 Bonus - 250000", "students_selected": 0},
    {"notification_date": "2025-08-20", "company_name": "E2E Networks", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "7", "job_roles": "Associate Software Engineer", "ctc_stipend": "CTC: ₹12,00,000\nStipend: ₹48,200\nCTC = Fixed - 1000000 - 1300000", "students_selected": 5},
    {"notification_date": "2025-08-05", "company_name": "Tekion", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE", "eligibility_cgpa": "7", "job_roles": "Associate Software Engineer", "ctc_stipend": "CTC: ₹19,99,999.95\nStipend: ₹65,000\nFixed - 2000000", "students_selected": 5},
    {"notification_date": "2025-08-05", "company_name": "Signzy", "type_of_offer": "SLI + PPO based on Performance", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "6.5", "job_roles": "MERN Stack Intern", "ctc_stipend": "Stipend: ₹40,000\nStipend - 35k fixed", "students_selected": 0},
    {"notification_date": "2025-07-29", "company_name": "Whatfix(Quiko)", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "7", "job_roles": "Software Engineer", "ctc_stipend": "CTC: ₹16,00,000\nStipend: ₹50,000\nFixed - 1300000, Variable Pay bonus - 300000", "students_selected": 4},
    {"notification_date": "2025-07-28", "company_name": "Eatclub", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "6.5", "job_roles": "SDE", "ctc_stipend": "CTC: ₹22,00,000\nStipend: ₹40,000\nFixed - 1000000 ESOPS - 1000000 Variable Bonus - 200000", "students_selected": 5},
    {"notification_date": "2025-07-22", "company_name": "MakeMyTrip", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, CCE", "eligibility_cgpa": "By Company - 5, after shortlisting 8 for Girls, 8.5 for Boys", "job_roles": "Software Engineer", "ctc_stipend": "CTC: ₹22,00,000\nStipend: ₹50,000\nFixed - 1200000 RSUs- 1000000", "students_selected": 2},
    {"notification_date": "2025-07-16", "company_name": "Sprinklr", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, CCE", "eligibility_cgpa": "7", "job_roles": "Cloud Engineer", "ctc_stipend": "CTC: ₹18,00,000\nStipend: ₹50,000\nFixed - 1500000 ESOPs - 300000", "students_selected": 2},
    {"notification_date": "2025-07-16", "company_name": "Addverb Technologies", "type_of_offer": "SLI + FTE", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "6", "job_roles": "Software Developer, Mobile Robotics, R&D Mechanical, Intern of all roles", "ctc_stipend": "CTC: ₹16,00,447\nStipend: ₹25,000\nFixed - 1045440", "students_selected": 7},
    {"notification_date": "2025-07-16", "company_name": "Triumph Motorcycles", "type_of_offer": "SLI + FTE", "branches_allowed": "Mechanical", "eligibility_cgpa": "5", "job_roles": "Graduate Engineer Trainee", "ctc_stipend": "CTC: ₹12,50,000\nStipend: ₹50,000", "students_selected": 4},
    {"notification_date": "2025-05-27", "company_name": "Bajaj Finserv Health Limited", "type_of_offer": "SLI + Performance Based PPO", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "5", "job_roles": "Backend Developer(Java)", "ctc_stipend": "CTC: ₹12,20,000\nStipend: ₹35,000", "students_selected": 2},
    {"notification_date": "2025-05-05", "company_name": "Media.net", "type_of_offer": "Summer Intern", "branches_allowed": "CSE, ECE, CCE", "eligibility_cgpa": "6", "job_roles": "SDE Intern", "ctc_stipend": "Stipend: ₹1,00,000\nPPO Converted", "students_selected": 1},
    {"notification_date": "2024-10-05", "company_name": "BNY Mellon", "type_of_offer": "Intern + PPO", "branches_allowed": "CSE", "eligibility_cgpa": "7.5", "job_roles": "CSE, CCE, ECE", "ctc_stipend": "CTC: ₹22,00,000\nStipend: ₹75,000", "students_selected": 4},
    {"notification_date": "2024-02-19", "company_name": "Deloitte", "type_of_offer": "Intern + PPO", "branches_allowed": "CSE, ECE, CCE, Mech", "eligibility_cgpa": "6", "job_roles": "Product Engineer, DataScience, UI/UX", "ctc_stipend": "CTC: ₹12,50,000\nStipend: ₹30,000", "students_selected": 21},
]

def seed_database():
    db = SessionLocal()
    try:
        # Check if data already exists
        count = db.query(Company).count()
        if count > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        # Add all companies
        for item in sample_data:
            # Create a copy to avoid modifying the original
            company_data = item.copy()
            # Convert date string to date object
            if isinstance(company_data['notification_date'], str):
                company_data['notification_date'] = datetime.strptime(company_data['notification_date'], '%Y-%m-%d').date()
            company = Company(**company_data)
            db.add(company)
        
        db.commit()
        print(f"Successfully added {len(sample_data)} companies to the database!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

