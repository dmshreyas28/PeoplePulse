"""Data preprocessing module."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTE
from typing import Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Handles data preprocessing and feature engineering."""
    
    def __init__(self, config: dict):
        """Initialize preprocessor with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with loaded data
        """
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with missing values handled
        """
        logger.info("Handling missing values")
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            logger.info(f"Found {missing.sum()} missing values")
            
            # Fill numeric columns with median
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(df) > 1:
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            else:
                # For single-row DataFrame, fill with the row's own values or 0
                df[numeric_cols] = df[numeric_cols].fillna(0)
            
            # Fill categorical columns with mode
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if len(df) > 1 and not df[col].mode().empty:
                    df[col] = df[col].fillna(df[col].mode()[0])
                else:
                    # For single-row or empty mode, fill with most common value or 'Unknown'
                    df[col] = df[col].fillna('Unknown')
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create derived features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional features
        """
        logger.info("Engineering features")
        
        df = df.copy()
        
        # Tenure ratio
        if 'YearsAtCompany' in df.columns and 'Age' in df.columns:
            df['TenureRatio'] = df['YearsAtCompany'] / (df['Age'] - 18 + 1)
        
        # Promotion rate
        if 'YearsSinceLastPromotion' in df.columns and 'YearsAtCompany' in df.columns:
            df['PromotionRate'] = df['YearsAtCompany'] / (df['YearsSinceLastPromotion'] + 1)
        
        # Income per age
        if 'MonthlyIncome' in df.columns and 'Age' in df.columns:
            df['IncomePerAge'] = df['MonthlyIncome'] / df['Age']
        
        # Job hopping indicator
        if 'NumCompaniesWorked' in df.columns and 'Age' in df.columns:
            df['JobHoppingRate'] = df['NumCompaniesWorked'] / (df['Age'] - 18 + 1)
        
        # Average satisfaction
        satisfaction_cols = [
            'JobSatisfaction', 'WorkLifeBalance', 
            'EnvironmentSatisfaction', 'RelationshipSatisfaction'
        ]
        available_cols = [col for col in satisfaction_cols if col in df.columns]
        if available_cols:
            df['AvgSatisfaction'] = df[available_cols].mean(axis=1)
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Encode categorical variables.
        
        Args:
            df: Input DataFrame
            fit: Whether to fit encoders (True for training, False for inference)
            
        Returns:
            DataFrame with encoded categorical variables
        """
        logger.info("Encoding categorical variables")
        
        df = df.copy()
        
        # Get all object/string columns
        string_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Encode all string columns
        for col in string_cols:
            if col in df.columns:
                if fit:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        # Handle unseen categories
                        le = self.label_encoders[col]
                        df[col] = df[col].astype(str).apply(
                            lambda x: le.transform([x])[0] if x in le.classes_ else -1
                        )
                    else:
                        # If encoder doesn't exist, encode as -1
                        df[col] = -1
        
        return df
    
    def scale_features(self, X: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Scale numeric features.
        
        Args:
            X: Feature DataFrame
            fit: Whether to fit scaler
            
        Returns:
            Scaled features as numpy array
        """
        logger.info("Scaling features")
        
        # If not fitting and we have feature_names, reorder columns to match training
        if not fit and self.feature_names:
            # Only keep columns that exist in training features
            missing_cols = [col for col in self.feature_names if col not in X.columns]
            if missing_cols:
                logger.warning(f"Missing columns: {missing_cols}")
                # Add missing columns with zeros
                for col in missing_cols:
                    X[col] = 0
            
            # Reorder to match training
            X = X[self.feature_names]
        
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def handle_imbalance(
        self, 
        X: np.ndarray, 
        y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Handle class imbalance using SMOTE.
        
        Args:
            X: Features
            y: Target variable
            
        Returns:
            Resampled X and y
        """
        if not self.config['preprocessing'].get('handle_imbalance', False):
            return X, y
        
        logger.info("Handling class imbalance with SMOTE")
        
        smote = SMOTE(random_state=self.config['preprocessing']['random_state'])
        X_resampled, y_resampled = smote.fit_resample(X, y)
        
        logger.info(f"Original samples: {len(X)}, Resampled: {len(X_resampled)}")
        
        return X_resampled, y_resampled
    
    def prepare_data(
        self, 
        df: pd.DataFrame,
        target_col: str = 'Attrition',
        fit: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Complete preprocessing pipeline.
        
        Args:
            df: Input DataFrame
            target_col: Name of target column
            fit: Whether to fit transformers
            
        Returns:
            Tuple of (X, y)
        """
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Separate features and target
        if target_col in df.columns:
            # Encode target if it's categorical
            if df[target_col].dtype == 'object':
                df[target_col] = (df[target_col] == 'Yes').astype(int)
            
            y = df[target_col].values
            X = df.drop(columns=[target_col])
        else:
            y = None
            X = df
        
        # Remove non-feature columns
        cols_to_drop = ['EmployeeID', 'EmployeeNumber', 'employee_id']
        X = X.drop(columns=[col for col in cols_to_drop if col in X.columns])
        
        # Encode categorical variables (only once)
        X = self.encode_categorical(X, fit=fit)
        
        # Store feature names
        if fit:
            self.feature_names = X.columns.tolist()
        
        # Scale features
        X = self.scale_features(X, fit=fit)
        
        return X, y
