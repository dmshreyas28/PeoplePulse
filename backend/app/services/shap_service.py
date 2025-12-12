"""SHAP explanation service."""
import shap
import numpy as np
import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ShapService:
    """Service for generating SHAP explanations."""
    
    def __init__(self, model):
        """Initialize SHAP service.
        
        Args:
            model: Trained ML model
        """
        self.model = model
        self.explainer = None
        self._initialize_explainer()
    
    def _initialize_explainer(self):
        """Initialize the SHAP explainer based on model type."""
        try:
            # Try TreeExplainer for tree-based models (XGBoost, LightGBM, RandomForest)
            self.explainer = shap.TreeExplainer(self.model)
            logger.info("Initialized TreeExplainer")
        except Exception as e:
            logger.warning(f"TreeExplainer failed: {e}. Falling back to KernelExplainer")
            # Fallback to KernelExplainer for other models
            # Note: This requires background data, which should be provided
            self.explainer = None
    
    def explain_prediction(
        self, 
        X: pd.DataFrame,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate SHAP explanations for a prediction.
        
        Args:
            X: Input features as DataFrame
            top_n: Number of top features to return
            
        Returns:
            List of dictionaries with feature, value, and impact
        """
        if self.explainer is None:
            logger.warning("SHAP explainer not initialized")
            return []
        
        try:
            # Calculate SHAP values
            shap_values = self.explainer.shap_values(X)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                # Binary classification - use positive class
                shap_values = shap_values[1]
            
            # Get feature names
            feature_names = X.columns.tolist()
            feature_values = X.iloc[0].tolist()
            
            # Combine into list of dicts
            explanations = []
            for feat, val, shap_val in zip(feature_names, feature_values, shap_values[0]):
                explanations.append({
                    'feature': feat,
                    'value': float(val),
                    'impact': float(shap_val)
                })
            
            # Sort by absolute impact
            explanations.sort(key=lambda x: abs(x['impact']), reverse=True)
            
            # Return top N
            return explanations[:top_n]
            
        except Exception as e:
            logger.error(f"Error generating SHAP explanations: {str(e)}")
            return []
    
    def get_feature_importance(self, X: pd.DataFrame) -> Dict[str, float]:
        """Get global feature importance.
        
        Args:
            X: Sample dataset
            
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if self.explainer is None:
            return {}
        
        try:
            shap_values = self.explainer.shap_values(X)
            
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            
            # Calculate mean absolute SHAP value for each feature
            importance = np.abs(shap_values).mean(axis=0)
            
            feature_importance = dict(zip(X.columns, importance))
            
            return feature_importance
            
        except Exception as e:
            logger.error(f"Error calculating feature importance: {str(e)}")
            return {}


# Global SHAP service instance
_shap_service: ShapService = None


def get_shap_service(model=None) -> ShapService:
    """Get or create the global SHAP service instance.
    
    Args:
        model: ML model (required on first call)
        
    Returns:
        ShapService instance
    """
    global _shap_service
    
    if _shap_service is None:
        if model is None:
            raise ValueError("model required for first initialization")
        _shap_service = ShapService(model)
    
    return _shap_service
