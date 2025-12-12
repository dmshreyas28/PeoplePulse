"""Simulation router endpoints."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
import logging

from ..services import get_model_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/simulate", tags=["Simulations"])


class SimulationRequest(BaseModel):
    """Request for intervention simulation."""
    
    employee_id: str
    current_data: Dict[str, Any]
    proposed_changes: Dict[str, Any]


class SimulationResponse(BaseModel):
    """Response from intervention simulation."""
    
    employee_id: str
    original_probability: float
    new_probability: float
    probability_change: float
    improvement_percent: float
    recommended: bool


@router.post("/intervention", response_model=SimulationResponse)
async def simulate_intervention(request: SimulationRequest):
    """Simulate the effect of retention interventions.
    
    Args:
        request: Current employee data and proposed changes
        
    Returns:
        Comparison of original and projected probabilities
    """
    try:
        # Get model service
        model_service = get_model_service()
        
        # Simulate intervention
        original_prob, new_prob = model_service.simulate_intervention(
            request.current_data,
            request.proposed_changes
        )
        
        # Calculate change
        prob_change = new_prob - original_prob
        improvement_percent = (prob_change / original_prob * 100) if original_prob > 0 else 0
        
        # Determine if intervention is recommended
        recommended = prob_change < -0.05  # At least 5% reduction
        
        response = SimulationResponse(
            employee_id=request.employee_id,
            original_probability=round(original_prob, 4),
            new_probability=round(new_prob, 4),
            probability_change=round(prob_change, 4),
            improvement_percent=round(improvement_percent, 2),
            recommended=recommended
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Simulation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}"
        )


@router.post("/compare")
async def compare_scenarios(
    employee_id: str,
    current_data: Dict[str, Any],
    scenarios: list[Dict[str, Any]]
):
    """Compare multiple intervention scenarios.
    
    Args:
        employee_id: Employee identifier
        current_data: Current employee data
        scenarios: List of scenario changes to compare
        
    Returns:
        Comparison of all scenarios
    """
    try:
        model_service = get_model_service()
        
        # Get baseline
        original_prob, _ = model_service.predict(current_data)
        
        results = []
        for idx, scenario in enumerate(scenarios):
            _, new_prob = model_service.simulate_intervention(
                current_data,
                scenario
            )
            
            results.append({
                'scenario_id': idx + 1,
                'changes': scenario,
                'original_probability': round(original_prob, 4),
                'new_probability': round(new_prob, 4),
                'improvement': round((original_prob - new_prob) * 100, 2)
            })
        
        # Sort by improvement
        results.sort(key=lambda x: x['improvement'], reverse=True)
        
        return {
            'employee_id': employee_id,
            'baseline_probability': round(original_prob, 4),
            'scenarios': results
        }
        
    except Exception as e:
        logger.error(f"Scenario comparison error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scenario comparison failed: {str(e)}"
        )
