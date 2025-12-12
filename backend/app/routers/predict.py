"""Prediction router endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..db import get_db
from ..models import Prediction
from ..schemas import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse, ShapValue
from ..services import get_model_service, get_shap_service, FeatureService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/predict", tags=["Predictions"])


@router.post("/employee", response_model=PredictResponse)
async def predict_single_employee(
    request: PredictRequest,
    db: Session = Depends(get_db)
):
    """Predict attrition for a single employee.
    
    Args:
        request: Employee data
        db: Database session
        
    Returns:
        Prediction with probability, risk level, and explanations
    """
    try:
        # Validate input
        is_valid, error_msg = FeatureService.validate_input(request.model_dump())
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Get model service
        model_service = get_model_service()
        
        # Make prediction
        employee_dict = request.model_dump()
        probability, features_df = model_service.predict(employee_dict)
        
        # Get risk level
        risk_level = model_service.get_risk_level(probability)
        
        # Generate SHAP explanations
        shap_service = get_shap_service(model_service.model)
        explanations = shap_service.explain_prediction(features_df, top_n=5)
        
        # Convert to ShapValue objects
        top_factors = [
            ShapValue(
                feature=exp['feature'],
                value=exp['value'],
                impact=exp['impact']
            )
            for exp in explanations
        ]
        
        # Generate recommendations
        recommendation = FeatureService.get_recommendations(probability, explanations)
        
        # Save prediction to database
        db_prediction = Prediction(
            employee_id=request.employee_id,
            attrition_probability=probability,
            risk_level=risk_level,
            shap_values=explanations,
            top_factors=[exp for exp in explanations],
            model_version="v1.0"
        )
        db.add(db_prediction)
        db.commit()
        
        # Return response
        response = PredictResponse(
            employee_id=request.employee_id,
            attrition_probability=round(probability, 4),
            risk_level=risk_level,
            top_factors=top_factors,
            confidence=1.0 - abs(probability - 0.5) * 2,  # Simple confidence metric
            recommendation=recommendation
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {type(e).__name__}: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {type(e).__name__}: {str(e)}"
        )


@router.post("/batch", response_model=BatchPredictResponse)
async def predict_batch(
    request: BatchPredictRequest,
    db: Session = Depends(get_db)
):
    """Predict attrition for multiple employees.
    
    Args:
        request: List of employee data
        db: Database session
        
    Returns:
        Batch prediction results
    """
    try:
        predictions = []
        high_risk_count = 0
        
        for employee in request.employees:
            # Predict for each employee
            prediction = await predict_single_employee(employee, db)
            predictions.append(prediction)
            
            if prediction.risk_level == "High":
                high_risk_count += 1
        
        response = BatchPredictResponse(
            predictions=predictions,
            total_count=len(predictions),
            high_risk_count=high_risk_count
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Batch prediction error: {type(e).__name__}: {str(e)}")
        logger.exception("Full batch traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {type(e).__name__}: {str(e)}"
        )


@router.get("/history/{employee_id}")
async def get_prediction_history(
    employee_id: str,
    db: Session = Depends(get_db)
):
    """Get prediction history for an employee.
    
    Args:
        employee_id: Employee identifier
        db: Database session
        
    Returns:
        List of historical predictions
    """
    predictions = db.query(Prediction).filter(
        Prediction.employee_id == employee_id
    ).order_by(Prediction.created_at.desc()).limit(10).all()
    
    return predictions
