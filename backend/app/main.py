from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import re
from statistics import median

from app.database import get_db, init_db
from app.models import Company
from app.schemas import Company as CompanySchema, CompanyCreate, CompanyUpdate
from app.config import settings

app = FastAPI(title="Placement Tracker API")

# CORS middleware
# Allow GitHub Pages and other common deployment origins
import os
cors_origins = [
    "http://localhost:3000",
    "https://lnmiit-placement-tracker-2026.onrender.com",
    "https://lnmiit-placement-tracker-2026-1.onrender.com",
]

# Add GitHub Pages origin if specified
github_pages_url = os.getenv("GITHUB_PAGES_URL")
if github_pages_url:
    cors_origins.append(github_pages_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    # Allow all GitHub Pages subdomains (https://username.github.io or custom domain)
    allow_origin_regex=r"https://.*\.github\.io.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()
    # Seed database if empty (important for fresh deployments)
    try:
        from app.seed import seed_database
        seed_database()
    except Exception as e:
        # Don't fail startup if seeding fails, but log it
        print(f"Warning: Could not seed database on startup: {e}")


# Authorization dependency: require admin token for write operations
def admin_required(
    x_admin_token: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    token = None
    if x_admin_token:
        token = x_admin_token.strip()
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()

    if not token or token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin privileges required")


@app.get("/api/auth/check", dependencies=[Depends(admin_required)])
def check_admin():
    return {"ok": True}

@app.get("/")
def read_root():
    return {"message": "Placement Tracker API"}

@app.get("/api/debug/db-info")
def get_db_info():
    """Debug endpoint to check database location"""
    from app.database import DATABASE_URL, DB_FILE
    import os
    db_exists = DB_FILE.exists() if DB_FILE else False
    db_size = DB_FILE.stat().st_size if (DB_FILE and DB_FILE.exists()) else 0
    db_type = "PostgreSQL/External" if (DB_FILE is None or "postgresql" in DATABASE_URL.lower()) else "SQLite"
    return {
        "database_type": db_type,
        "database_url": DATABASE_URL,
        "database_file": str(DB_FILE) if DB_FILE else "Using external database (PostgreSQL, etc.)",
        "database_exists": db_exists,
        "database_size_bytes": db_size,
        "current_working_directory": os.getcwd(),
        "is_cloud_environment": any(os.path.exists(p) for p in ["/opt/render/project/src", "/app"]),
    }

@app.get("/api/companies", response_model=List[CompanySchema])
def get_companies(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@app.get("/api/companies/{company_id}", response_model=CompanySchema)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.post("/api/companies", response_model=CompanySchema, dependencies=[Depends(admin_required)])
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    try:
        db_company = Company(**company.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating company: {str(e)}")

@app.put("/api/companies/{company_id}", response_model=CompanySchema, dependencies=[Depends(admin_required)])
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    try:
        db_company = db.query(Company).filter(Company.id == company_id).first()
        if not db_company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        update_data = company.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        
        db.commit()
        db.refresh(db_company)
        return db_company
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating company: {str(e)}")

@app.delete("/api/companies/{company_id}", dependencies=[Depends(admin_required)])
def delete_company(company_id: int, db: Session = Depends(get_db)):
    try:
        db_company = db.query(Company).filter(Company.id == company_id).first()
        if not db_company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        db.delete(db_company)
        db.commit()
        return {"message": "Company deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting company: {str(e)}")

def extract_ctc_value(text: str) -> float | None:
    """Extract CTC value from text like 'CTC: ₹12,50,000' or 'Fixed - 1150000'"""
    if not text:
        return None
    
    # Look for CTC with rupee symbol
    ctc_match = re.search(r'CTC:\s*₹?\s*([\d,]+)', text, re.IGNORECASE)
    if ctc_match:
        return float(ctc_match.group(1).replace(',', ''))
    
    # Look for "Fixed - XXXXX" pattern (without rupee symbol)
    fixed_match = re.search(r'Fixed\s*-\s*₹?\s*([\d,]+)', text, re.IGNORECASE)
    if fixed_match:
        return float(fixed_match.group(1).replace(',', ''))
    
    # Look for any large number (greater than 1 lakh)
    all_numbers = re.findall(r'₹?\s*([\d,]+)', text)
    for num_str in all_numbers:
        num = float(num_str.replace(',', ''))
        if num > 100000:  # Likely a CTC
            return num
    
    return None

def extract_stipend_value(text: str) -> float | None:
    """Extract stipend value from text"""
    if not text:
        return None
    
    # Look for stipend explicitly
    stipend_match = re.search(r'Stipend:\s*₹?\s*([\d,]+)', text, re.IGNORECASE)
    if stipend_match:
        return float(stipend_match.group(1).replace(',', ''))
    
    return None

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    companies = db.query(Company).all()

    def parse_amount(token: str) -> float | None:
        if not token:
            return None
        t = token.replace(",", "").strip().lower()
        m = re.match(r"^(\d+(?:\.\d+)?)(k)?$", t)
        if not m:
            return None
        val = float(m.group(1))
        if m.group(2):
            val *= 1000
        return val

    def find_amount(pattern: str, text: str) -> float | None:
        m = re.search(pattern, text, flags=re.I)
        if not m:
            return None
        raw = m.group(1)
        # support tokens like 35k
        if re.search(r"\d\s*[kK]", raw):
            raw = raw.replace(" ", "")
        return parse_amount(raw)

    if not companies:
        return {
            "total_unique_companies": 0,
            "on_campus": 0,
            "ppo": 0,
            "average_stipend": 0,
            "average_ctc": 0,
            "median_ctc": 0,
            "average_ctc_weighted": 0,
            "students_selected": 0,
            "intern_count": 0,
            "fte_count": 0,
            "intern_fte_count": 0,
        }

    # Unique companies and PPO
    unique_companies = set(c.company_name for c in companies)
    total_unique = len(unique_companies)
    ppo_count = len(
        set(c.company_name for c in companies if "PPO" in c.type_of_offer.upper())
    )
    on_campus_count = total_unique - ppo_count

    stipend_weighted: list[tuple[float, int]] = []
    ctc_simple: list[float] = []
    fixed_weighted: list[tuple[float, int]] = []

    for c in companies:
        text = (c.ctc_stipend or "").strip()

        # Stipend parsing: explicit only; include zeros only when explicitly 0
        stipend = None
        # Stipend: ₹1,00,000 or Stipend - 35k fixed
        stipend = find_amount(r"Stipend\s*[:\-]\s*₹?\s*([\d,]+(?:\.\d+)?|\d+(?:\.\d+)?\s*[kK])", text)
        if stipend is None:
            # sometimes just 'Stipend' line with amount after space
            stipend = find_amount(r"Stipend\s*₹?\s*([\d,]+(?:\.\d+)?|\d+(?:\.\d+)?\s*[kK])", text)
        if stipend is not None:
            stipend_weighted.append((stipend, c.students_selected))

        # CTC parsing: CTC: ₹x
        ctc = find_amount(r"CTC\s*[:\-]\s*₹?\s*([\d,]+(?:\.\d+)?|\d+(?:\.\d+)?\s*[kK])", text)
        if ctc is not None:
            ctc_simple.append(ctc)

        # Fixed parsing: Fixed - amount OR Fixed - same as CTC
        fixed_match = re.search(r"Fixed\s*[-:]\s*(same as CTC|₹?\s*[\d,]+(?:\.\d+)?|\d+(?:\.\d+)?\s*[kK])", text, flags=re.I)
        fixed_val = None
        if fixed_match:
            fixed_raw = fixed_match.group(1)
            if isinstance(fixed_raw, str) and fixed_raw.strip().lower().startswith("same"):
                fixed_val = ctc
            else:
                fixed_val = parse_amount(fixed_raw)
        # If no explicit Fixed but only CTC given, do not assume Fixed; keep None
        if fixed_val is not None:
            fixed_weighted.append((fixed_val, c.students_selected))

    def weighted_avg(pairs: list[tuple[float, int]]) -> float:
        if not pairs:
            return 0.0
        total_value = sum(v * w for v, w in pairs)
        total_weight = sum(w for _, w in pairs)
        return (total_value / total_weight) if total_weight > 0 else 0.0

    def simple_avg(values: list[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)

    # Count students by type
    intern_count = sum(
        c.students_selected
        for c in companies
        if "intern" in c.type_of_offer.lower() and "fte" not in c.type_of_offer.lower()
    )
    fte_count = sum(
        c.students_selected
        for c in companies
        if "fte" in c.type_of_offer.lower() and "intern" not in c.type_of_offer.lower()
    )
    intern_fte_count = sum(
        c.students_selected
        for c in companies
        if (
            "intern+fte" in c.type_of_offer.lower()
            or ("intern" in c.type_of_offer.lower() and "fte" in c.type_of_offer.lower())
        )
    )

    total_students = sum(c.students_selected for c in companies)

    # Median package secured: use Fixed values median when available
    fixed_values_only = [v for v, _ in fixed_weighted]
    median_package = median(fixed_values_only) if fixed_values_only else 0.0

    return {
        "total_unique_companies": total_unique,
        "on_campus": on_campus_count,
        "ppo": ppo_count,
        # Weighted average stipend across entries that explicitly report stipend
        "average_stipend": weighted_avg(stipend_weighted),
        # Average CTC as simple mean of explicit CTC amounts
        "average_ctc": simple_avg(ctc_simple),
        # Median package secured: based on Fixed values
        "median_ctc": median_package,
        # Average package secured (weighted): use Fixed values
        "average_ctc_weighted": weighted_avg(fixed_weighted),
        "students_selected": total_students,
        "intern_count": intern_count,
        "fte_count": fte_count,
        "intern_fte_count": intern_fte_count,
    }
