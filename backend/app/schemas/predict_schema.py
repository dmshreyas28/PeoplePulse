"""Prediction Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class PredictRequest(BaseModel):
    """Request schema for prediction."""
    
    employee_id: str
    age: int
    gender: str
    department: str
    job_role: str
    education: int
    education_field: str
    years_at_company: int
    years_in_current_role: int
    years_since_last_promotion: int
    years_with_curr_manager: int
    num_companies_worked: int
    monthly_income: float
    percent_salary_hike: int
    stock_option_level: int
    training_times_last_year: int
    job_satisfaction: int
    work_life_balance: int
    environment_satisfaction: int
    relationship_satisfaction: int
    performance_rating: int
    business_travel: str
    distance_from_home: int
    marital_status: str
    overtime: str
    # Additional IBM dataset fields
    daily_rate: Optional[int] = 800
    hourly_rate: Optional[int] = 65
    monthly_rate: Optional[int] = 14000
    job_level: Optional[int] = 2
    job_involvement: Optional[int] = 3
    total_working_years: Optional[int] = 5
    employee_count: Optional[int] = 1
    standard_hours: Optional[int] = 80
    over_18: Optional[str] = "Y"
    employee_number: Optional[int] = None


class ShapValue(BaseModel):
    """SHAP value explanation."""
    
    feature: str
    value: float
    impact: float  # SHAP value


class PredictResponse(BaseModel):
    """Response schema for prediction."""
    
    employee_id: str
    attrition_probability: float = Field(..., ge=0, le=1)
    risk_level: str = Field(..., pattern="^(Low|Medium|High)$")
    top_factors: List[ShapValue]
    confidence: float = Field(..., ge=0, le=1)
    recommendation: Optional[str] = None


class BatchPredictRequest(BaseModel):
    """Request schema for batch prediction."""
    
    employees: List[PredictRequest]


class BatchPredictResponse(BaseModel):
    """Response schema for batch prediction."""
    
    predictions: List[PredictResponse]
    total_count: int
    high_risk_count: int
