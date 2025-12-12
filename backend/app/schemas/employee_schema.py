"""Employee Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    """Base employee schema."""
    
    employee_id: str = Field(..., description="Unique employee identifier")
    age: int = Field(..., ge=18, le=100)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    department: str
    job_role: str
    education: int = Field(..., ge=1, le=5)
    education_field: str
    years_at_company: int = Field(..., ge=0)
    years_in_current_role: int = Field(..., ge=0)
    years_since_last_promotion: int = Field(..., ge=0)
    years_with_curr_manager: int = Field(..., ge=0)
    num_companies_worked: int = Field(..., ge=0)
    monthly_income: float = Field(..., gt=0)
    percent_salary_hike: int = Field(..., ge=0, le=100)
    stock_option_level: int = Field(..., ge=0, le=3)
    training_times_last_year: int = Field(..., ge=0)
    job_satisfaction: int = Field(..., ge=1, le=4)
    work_life_balance: int = Field(..., ge=1, le=4)
    environment_satisfaction: int = Field(..., ge=1, le=4)
    relationship_satisfaction: int = Field(..., ge=1, le=4)
    performance_rating: int = Field(..., ge=1, le=4)
    business_travel: str = Field(..., pattern="^(Non-Travel|Travel_Rarely|Travel_Frequently)$")
    distance_from_home: int = Field(..., ge=0)
    marital_status: str = Field(..., pattern="^(Single|Married|Divorced)$")
    overtime: str = Field(..., pattern="^(Yes|No)$")


class EmployeeCreate(EmployeeBase):
    """Schema for creating an employee."""
    pass


class EmployeeResponse(EmployeeBase):
    """Schema for employee response."""
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
