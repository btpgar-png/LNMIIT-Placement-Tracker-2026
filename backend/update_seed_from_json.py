"""
Script to update seed.py from a companies.json file
Use this if you manually exported the companies data.
"""
import json
from datetime import datetime
import os

JSON_FILE = "companies.json"

if not os.path.exists(JSON_FILE):
    print(f"✗ Error: {JSON_FILE} not found!")
    print(f"Please export the companies data and save it as {JSON_FILE}")
    print("\nTo export:")
    print("1. Open browser console on your site")
    print("2. Run: fetch('/api/companies').then(r => r.json()).then(d => console.log(JSON.stringify(d, null, 2)))")
    print("3. Copy the output and save as companies.json")
    exit(1)

try:
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    print(f"✓ Loaded {len(companies)} companies from {JSON_FILE}")
    
    # Convert to seed format
    sample_data = []
    for company in companies:
        # Convert date object to string if needed
        notification_date = company.get('notification_date')
        if isinstance(notification_date, str):
            date_str = notification_date
        else:
            date_str = notification_date.strftime('%Y-%m-%d') if hasattr(notification_date, 'strftime') else str(notification_date)
        
        company_entry = {
            "notification_date": date_str,
            "company_name": company.get('company_name', ''),
            "type_of_offer": company.get('type_of_offer', ''),
            "branches_allowed": company.get('branches_allowed', ''),
            "eligibility_cgpa": company.get('eligibility_cgpa', ''),
            "job_roles": company.get('job_roles', ''),
            "ctc_stipend": company.get('ctc_stipend', ''),
            "students_selected": company.get('students_selected', 0),
        }
        sample_data.append(company_entry)
    
    # Generate seed.py content
    seed_content = f'''from app.models import Company
from app.database import SessionLocal
from datetime import datetime, date

# Sample data - Auto-generated from live database ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
sample_data = [
'''
    
    for company in sample_data:
        # Format the entry with proper escaping
        company_str = f'''    {{"notification_date": "{company['notification_date']}", "company_name": {json.dumps(company['company_name'])}, "type_of_offer": {json.dumps(company['type_of_offer'])}, "branches_allowed": {json.dumps(company['branches_allowed'])}, "eligibility_cgpa": {json.dumps(company['eligibility_cgpa'])}, "job_roles": {json.dumps(company['job_roles'])}, "ctc_stipend": {json.dumps(company['ctc_stipend'])}, "students_selected": {company['students_selected']}}},
'''
        seed_content += company_str
    
    seed_content += ''']

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
            # Ensure process field is set (default to "Completed")
            if 'process' not in company_data:
                company_data['process'] = "Completed"
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
    # Initialize database first if running standalone
    from app.database import init_db
    init_db()
    seed_database()
'''
    
    # Write to seed.py
    with open('app/seed.py', 'w', encoding='utf-8') as f:
        f.write(seed_content)
    
    print(f"✓ Successfully updated app/seed.py with {len(sample_data)} companies!")
    print("✓ All your manually added companies are now in the seed file!")
    print("✓ They will persist even if the database is reset.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

