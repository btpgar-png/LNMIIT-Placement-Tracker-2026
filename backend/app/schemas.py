from pydantic import BaseModel
from datetime import date
from typing import Optional

class CompanyBase(BaseModel):
    notification_date: date
    company_name: str
    type_of_offer: str
    branches_allowed: Optional[str] = None
    eligibility_cgpa: Optional[str] = None
    job_roles: str
    ctc_stipend: str
    students_selected: int
    process: Optional[str] = "Completed"

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    notification_date: Optional[date] = None
    company_name: Optional[str] = None
    type_of_offer: Optional[str] = None
    branches_allowed: Optional[str] = None
    eligibility_cgpa: Optional[str] = None
    job_roles: Optional[str] = None
    ctc_stipend: Optional[str] = None
    students_selected: Optional[int] = None
    process: Optional[str] = None

class Company(CompanyBase):
    id: int
    
    class Config:
        from_attributes = True

