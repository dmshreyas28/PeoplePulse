"""Prediction database model."""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from ..db import Base


class Prediction(Base):
    """Prediction history table model."""
    
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True, nullable=False)
    attrition_probability = Column(Float, nullable=False)
    risk_level = Column(String)  # Low, Medium, High
    shap_values = Column(JSON)  # Store SHAP explanations as JSON
    top_factors = Column(JSON)  # Top contributing factors
    model_version = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
