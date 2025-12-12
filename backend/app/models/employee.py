"""Employee database model."""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from ..db import Base


class Employee(Base):
    """Employee table model."""
    
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    department = Column(String)
    job_role = Column(String)
    education = Column(Integer)
    education_field = Column(String)
    years_at_company = Column(Integer)
    years_in_current_role = Column(Integer)
    years_since_last_promotion = Column(Integer)
    years_with_curr_manager = Column(Integer)
    num_companies_worked = Column(Integer)
    monthly_income = Column(Float)
    percent_salary_hike = Column(Integer)
    stock_option_level = Column(Integer)
    training_times_last_year = Column(Integer)
    job_satisfaction = Column(Integer)
    work_life_balance = Column(Integer)
    environment_satisfaction = Column(Integer)
    relationship_satisfaction = Column(Integer)
    performance_rating = Column(Integer)
    business_travel = Column(String)
    distance_from_home = Column(Integer)
    marital_status = Column(String)
    overtime = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
