"""
Script to fetch companies from live API and update seed.py
This ensures all manually added companies persist in the seed file.
"""
import requests
import json
from datetime import datetime

# Fetch companies from live API
API_URL = "https://lnmiit-placement-tracker-2026-1.onrender.com/api/companies"

# Try different possible endpoints
endpoints_to_try = [
    API_URL,
    API_URL.replace('/api/companies', '/companies'),
    "https://lnmiit-placement-tracker-2026-1.onrender.com/companies",
]

response = None
for endpoint in endpoints_to_try:
    try:
        print(f"Trying {endpoint}...")
        response = requests.get(endpoint, timeout=30, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            print(f"✓ Successfully connected to {endpoint}")
            break
    except Exception as e:
        print(f"  Failed: {e}")
        continue

if response and response.status_code == 200:
    try:
        companies = response.json()
        print(f"✓ Successfully fetched {len(companies)} companies")
        
        # Convert to seed format
        sample_data = []
        for company in companies:
            # Convert date object to string if needed
            notification_date = company.get('notification_date')
            if isinstance(notification_date, str):
                # Already a string, use as is
                date_str = notification_date
            else:
                # Convert date object to string
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
        print(f"✗ Error processing data: {e}")
        import traceback
        traceback.print_exc()
else:
        print(f"\n✗ Could not fetch from API (status: {response.status_code if response else 'No response'})")
        print("\n" + "="*60)
        print("MANUAL EXPORT INSTRUCTIONS:")
        print("="*60)
        print("1. Open your browser and go to:")
        print("   https://lnmiit-placement-tracker-2026-1.onrender.com/")
        print("\n2. Open Browser Console (F12 or Right-click > Inspect > Console)")
        print("\n3. Paste and run this JavaScript code:")
        print("-"*60)
        print("""
fetch('/api/companies')
  .then(r => r.json())
  .then(data => {
    console.log(JSON.stringify(data, null, 2));
    // Copy the output and save to companies.json
  });
""")
        print("-"*60)
        print("\n4. Copy the JSON output and save it as 'companies.json' in the backend folder")
        print("5. Then run: python update_seed_from_json.py")
        print("="*60)

