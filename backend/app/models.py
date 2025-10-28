from sqlalchemy import Column, Integer, String, Date, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    notification_date = Column(Date, nullable=False)
    company_name = Column(String(255), nullable=False)
    type_of_offer = Column(String(100), nullable=False)
    branches_allowed = Column(Text)
    eligibility_cgpa = Column(String(50))
    job_roles = Column(Text, nullable=False)
    ctc_stipend = Column(Text, nullable=False)
    students_selected = Column(Integer, nullable=False)
    # New: tracking recruitment process status (Completed/Pending)
    process = Column(String(20), nullable=False, default="Completed", server_default="Completed")

