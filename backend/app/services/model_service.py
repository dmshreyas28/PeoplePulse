"""ML model service for loading and prediction."""
import os
import sys
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class ModelService:
    """Service for ML model operations."""
    
    def __init__(self, model_path: str):
        """Initialize the model service.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model_path = Path(model_path)
        self.model = None
        self.preprocessor = None
        self.feature_names = None
        
    def load_model(self) -> bool:
        """Load the trained model from disk.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not self.model_path.exists():
                logger.error(f"Model file not found at {self.model_path}")
                return False

            # The saved model artifact includes the DataPreprocessor from ml/pipeline.
            # Ensure ml/pipeline is on sys.path so joblib can deserialize it.
            # Prefer the ML_PIPELINE_PATH environment variable; fall back to paths relative
            # to the model file (works for both local development and Docker deployments
            # where ml/pipeline is mounted at /ml/pipeline).
            pipeline_candidates = [
                # Docker / explicit mount: /ml/pipeline
                Path('/ml/pipeline'),
                # Local development: <project_root>/ml/pipeline
                self.model_path.resolve().parent.parent / 'pipeline',
            ]
            extra_path = os.environ.get('ML_PIPELINE_PATH')
            if extra_path:
                pipeline_candidates.insert(0, Path(extra_path))

            for pipeline_path in pipeline_candidates:
                if pipeline_path.exists() and str(pipeline_path) not in sys.path:
                    sys.path.insert(0, str(pipeline_path))
                    logger.info(f"Added {pipeline_path} to sys.path for model deserialization")
                    break

            model_artifacts = joblib.load(self.model_path)
            
            # Handle both dict format (with preprocessor) and direct model format
            if isinstance(model_artifacts, dict):
                self.model = model_artifacts.get('model')
                self.preprocessor = model_artifacts.get('preprocessor')
                self.feature_names = model_artifacts.get('feature_names', [])
            else:
                # Legacy format - direct model
                self.model = model_artifacts
                if hasattr(self.model, 'feature_names_in_'):
                    self.feature_names = self.model.feature_names_in_
            
            logger.info(f"Model loaded successfully from {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def preprocess_input(self, employee_data: Dict[str, Any]) -> pd.DataFrame:
        """Preprocess employee data for prediction.
        
        Args:
            employee_data: Dictionary containing employee features
            
        Returns:
            Preprocessed DataFrame ready for prediction
        """
        # Column name mapping from API schema (snake_case) to dataset format (PascalCase)
        column_mapping = {
            'age': 'Age',
            'gender': 'Gender',
            'department': 'Department',
            'job_role': 'JobRole',
            'education': 'Education',
            'education_field': 'EducationField',
            'years_at_company': 'YearsAtCompany',
            'years_in_current_role': 'YearsInCurrentRole',
            'years_since_last_promotion': 'YearsSinceLastPromotion',
            'years_with_curr_manager': 'YearsWithCurrManager',
            'num_companies_worked': 'NumCompaniesWorked',
            'monthly_income': 'MonthlyIncome',
            'percent_salary_hike': 'PercentSalaryHike',
            'stock_option_level': 'StockOptionLevel',
            'training_times_last_year': 'TrainingTimesLastYear',
            'job_satisfaction': 'JobSatisfaction',
            'work_life_balance': 'WorkLifeBalance',
            'environment_satisfaction': 'EnvironmentSatisfaction',
            'relationship_satisfaction': 'RelationshipSatisfaction',
            'performance_rating': 'PerformanceRating',
            'business_travel': 'BusinessTravel',
            'distance_from_home': 'DistanceFromHome',
            'marital_status': 'MaritalStatus',
            'overtime': 'OverTime',
            'daily_rate': 'DailyRate',
            'hourly_rate': 'HourlyRate',
            'monthly_rate': 'MonthlyRate',
            'job_level': 'JobLevel',
            'job_involvement': 'JobInvolvement',
            'total_working_years': 'TotalWorkingYears',
            'employee_count': 'EmployeeCount',
            'standard_hours': 'StandardHours',
            'over_18': 'Over18',
            'employee_number': 'EmployeeNumber'
        }
        
        # Remove employee_id as it's not a feature
        features = {k: v for k, v in employee_data.items() if k != 'employee_id'}
        
        # Calculate TotalWorkingYears if not provided (approximate based on age and years_at_company)
        if features.get('total_working_years') is None:
            age = features.get('age', 30)
            years_at_company = features.get('years_at_company', 0)
            # Assume people start working around age 18-22, use age-20 as estimate
            features['total_working_years'] = max(years_at_company, age - 20)
        
        # Calculate EmployeeNumber if not provided
        if features.get('employee_number') is None:
            features['employee_number'] = hash(employee_data.get('employee_id', '')) % 100000
        
        # Set default values for fields that are always constant in IBM dataset
        if features.get('employee_count') is None:
            features['employee_count'] = 1
        if features.get('standard_hours') is None:
            features['standard_hours'] = 80
        if features.get('over_18') is None:
            features['over_18'] = 'Y'
        
        # Convert column names to match training data format
        features_mapped = {column_mapping.get(k, k): v for k, v in features.items()}
        
        # Convert to DataFrame
        df = pd.DataFrame([features_mapped])
        
        # If we have a preprocessor, use it
        if self.preprocessor:
            # The preprocessor's prepare_data returns (X, y), we only need X
            X, _ = self.preprocessor.prepare_data(df, fit=False)
            # Convert back to DataFrame if it's a numpy array
            if isinstance(X, np.ndarray):
                if self.feature_names:
                    X = pd.DataFrame(X, columns=self.feature_names)
                else:
                    X = pd.DataFrame(X)
            return X
        
        return df
    
    def predict(self, employee_data: Dict[str, Any]) -> Tuple[float, np.ndarray]:
        """Make prediction for a single employee.
        
        Args:
            employee_data: Dictionary containing employee features
            
        Returns:
            Tuple of (probability, prediction)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Preprocess input
        X = self.preprocess_input(employee_data)
        
        # Get prediction probability
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(X)[0]
            # Return probability of attrition (class 1)
            attrition_prob = proba[1] if len(proba) > 1 else proba[0]
        else:
            # Fallback for models without predict_proba
            pred = self.model.predict(X)[0]
            attrition_prob = float(pred)
        
        return float(attrition_prob), X
    
    def predict_batch(self, employees_data: list[Dict[str, Any]]) -> list[Tuple[float, np.ndarray]]:
        """Make predictions for multiple employees.
        
        Args:
            employees_data: List of employee data dictionaries
            
        Returns:
            List of (probability, features) tuples
        """
        results = []
        for employee_data in employees_data:
            prob, features = self.predict(employee_data)
            results.append((prob, features))
        
        return results
    
    def get_risk_level(self, probability: float) -> str:
        """Determine risk level from probability.
        
        Args:
            probability: Attrition probability
            
        Returns:
            Risk level: Low, Medium, or High
        """
        if probability < 0.3:
            return "Low"
        elif probability < 0.6:
            return "Medium"
        else:
            return "High"
    
    def simulate_intervention(
        self, 
        employee_data: Dict[str, Any],
        changes: Dict[str, Any]
    ) -> Tuple[float, float]:
        """Simulate the effect of interventions.
        
        Args:
            employee_data: Original employee data
            changes: Dictionary of feature changes to simulate
            
        Returns:
            Tuple of (original_prob, new_prob)
        """
        # Get original prediction
        original_prob, _ = self.predict(employee_data)
        
        # Apply changes
        modified_data = employee_data.copy()
        modified_data.update(changes)
        
        # Get new prediction
        new_prob, _ = self.predict(modified_data)
        
        return original_prob, new_prob


# Global model service instance
_model_service: ModelService = None


def get_model_service(model_path: str = None) -> ModelService:
    """Get or create the global model service instance.
    
    Args:
        model_path: Path to model file (required on first call)
        
    Returns:
        ModelService instance
    """
    global _model_service
    
    if _model_service is None:
        if model_path is None:
            raise ValueError("model_path required for first initialization")
        _model_service = ModelService(model_path)
        _model_service.load_model()
    
    return _model_service
