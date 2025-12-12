"""Feature engineering service."""
import pandas as pd
from typing import Dict, Any


class FeatureService:
    """Service for feature engineering and transformations."""
    
    @staticmethod
    def calculate_derived_features(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived features from raw data.
        
        Args:
            df: DataFrame with raw features
            
        Returns:
            DataFrame with additional derived features
        """
        df = df.copy()
        
        # Tenure-related features
        if 'years_at_company' in df.columns and 'age' in df.columns:
            df['tenure_ratio'] = df['years_at_company'] / (df['age'] - 18 + 1)
        
        # Career progression features
        if 'years_since_last_promotion' in df.columns and 'years_at_company' in df.columns:
            df['promotion_rate'] = df['years_at_company'] / (df['years_since_last_promotion'] + 1)
        
        # Income-related features
        if 'monthly_income' in df.columns and 'age' in df.columns:
            df['income_per_age'] = df['monthly_income'] / df['age']
        
        # Work stability
        if 'num_companies_worked' in df.columns and 'age' in df.columns:
            df['job_hopping_rate'] = df['num_companies_worked'] / (df['age'] - 18 + 1)
        
        # Satisfaction composite
        satisfaction_cols = [
            'job_satisfaction',
            'work_life_balance',
            'environment_satisfaction',
            'relationship_satisfaction'
        ]
        if all(col in df.columns for col in satisfaction_cols):
            df['avg_satisfaction'] = df[satisfaction_cols].mean(axis=1)
        
        return df
    
    @staticmethod
    def validate_input(employee_data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate employee input data.
        
        Args:
            employee_data: Dictionary of employee features
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = [
            'age', 'gender', 'department', 'job_role', 'education',
            'education_field', 'years_at_company', 'monthly_income'
        ]
        
        # Check required fields
        missing = [f for f in required_fields if f not in employee_data]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        
        # Validate ranges
        if employee_data.get('age', 0) < 18 or employee_data.get('age', 0) > 100:
            return False, "Age must be between 18 and 100"
        
        if employee_data.get('monthly_income', 0) <= 0:
            return False, "Monthly income must be positive"
        
        if employee_data.get('years_at_company', 0) < 0:
            return False, "Years at company cannot be negative"
        
        return True, ""
    
    @staticmethod
    def get_recommendations(
        probability: float,
        top_factors: list[Dict[str, Any]]
    ) -> str:
        """Generate retention recommendations based on prediction.
        
        Args:
            probability: Attrition probability
            top_factors: Top contributing factors
            
        Returns:
            Recommendation string
        """
        if probability < 0.3:
            return "Low risk. Continue regular engagement and development."
        
        recommendations = []
        
        # Analyze top factors
        for factor in top_factors[:3]:
            feature = factor['feature']
            impact = factor['impact']
            
            if 'satisfaction' in feature.lower() and impact > 0:
                recommendations.append("Address satisfaction concerns through surveys and 1-on-1s")
            
            if 'income' in feature.lower() and impact > 0:
                recommendations.append("Review compensation and consider salary adjustment")
            
            if 'promotion' in feature.lower() and impact > 0:
                recommendations.append("Discuss career development and promotion opportunities")
            
            if 'overtime' in feature.lower() and impact > 0:
                recommendations.append("Reduce overtime and improve work-life balance")
            
            if 'work_life_balance' in feature.lower() and impact > 0:
                recommendations.append("Offer flexible work arrangements")
        
        if not recommendations:
            recommendations.append("Schedule retention discussion with manager")
        
        return "; ".join(recommendations[:3])
