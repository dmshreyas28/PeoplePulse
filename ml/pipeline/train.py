"""Model training module."""
import yaml
import joblib
import json
import mlflow
import mlflow.xgboost
import mlflow.lightgbm
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, classification_report,
    confusion_matrix
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
import logging
import argparse

from preprocess import DataPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Handles model training and evaluation."""
    
    def __init__(self, config: dict):
        """Initialize trainer with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model = None
        self.preprocessor = DataPreprocessor(config)
        
    def create_model(self):
        """Create model based on configuration."""
        algorithm = self.config['model']['algorithm']
        params = self.config['model']['hyperparameters']
        
        logger.info(f"Creating {algorithm} model")
        
        if algorithm == 'xgboost':
            self.model = XGBClassifier(**params)
        elif algorithm == 'lightgbm':
            self.model = LGBMClassifier(**params)
        elif algorithm == 'random_forest':
            self.model = RandomForestClassifier(**params)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        return self.model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        logger.info("Training model...")
        
        if self.model is None:
            self.create_model()
        
        # Train model
        self.model.fit(X_train, y_train)
        
        logger.info("Training completed")
    
    def evaluate(
        self, 
        X_test: np.ndarray, 
        y_test: np.ndarray
    ) -> dict:
        """Evaluate model performance.
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of metrics
        """
        logger.info("Evaluating model...")
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        logger.info("Evaluation metrics:")
        for metric, value in metrics.items():
            logger.info(f"  {metric}: {value:.4f}")
        
        # Classification report
        logger.info("\nClassification Report:")
        logger.info("\n" + classification_report(y_test, y_pred))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"\nConfusion Matrix:\n{cm}")
        
        return metrics
    
    def cross_validate(self, X: np.ndarray, y: np.ndarray) -> dict:
        """Perform cross-validation.
        
        Args:
            X: Features
            y: Labels
            
        Returns:
            Cross-validation scores
        """
        cv_folds = self.config['training']['cv_folds']
        logger.info(f"Performing {cv_folds}-fold cross-validation")
        
        scores = cross_val_score(
            self.model, X, y, 
            cv=cv_folds, 
            scoring='roc_auc'
        )
        
        cv_results = {
            'cv_scores': scores.tolist(),
            'cv_mean': scores.mean(),
            'cv_std': scores.std()
        }
        
        logger.info(f"CV ROC-AUC: {scores.mean():.4f} (+/- {scores.std():.4f})")
        
        return cv_results
    
    def save_model(self, filepath: str):
        """Save trained model to disk.
        
        Args:
            filepath: Path to save model
        """
        logger.info(f"Saving model to {filepath}")
        
        # Create output directory if needed
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Save model and preprocessor together
        model_artifacts = {
            'model': self.model,
            'preprocessor': self.preprocessor,
            'feature_names': self.preprocessor.feature_names,
            'config': self.config
        }
        
        joblib.dump(model_artifacts, filepath)
        logger.info("Model saved successfully")
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from the model.
        
        Returns:
            DataFrame with feature importance
        """
        if hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
            feature_names = self.preprocessor.feature_names
            
            df = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            
            return df
        
        return pd.DataFrame()


def train_pipeline(config_path: str):
    """Main training pipeline.
    
    Args:
        config_path: Path to configuration file
    """
    # Load configuration
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize MLflow if configured
    if config['training'].get('use_mlflow', False):
        mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
        mlflow.set_experiment(config['mlflow']['experiment_name'])
        mlflow.start_run()
    
    try:
        # Create trainer
        trainer = ModelTrainer(config)
        
        # Load and preprocess data
        logger.info("Loading and preprocessing data...")
        df = trainer.preprocessor.load_data(config['data']['raw_path'])
        X, y = trainer.preprocessor.prepare_data(df, fit=True)
        
        # Split data
        test_size = config['preprocessing']['test_size']
        random_state = config['preprocessing']['random_state']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
        
        # Handle imbalance
        X_train, y_train = trainer.preprocessor.handle_imbalance(X_train, y_train)
        
        # Train model
        trainer.train(X_train, y_train)
        
        # Evaluate
        metrics = trainer.evaluate(X_test, y_test)
        
        # Cross-validation
        cv_results = trainer.cross_validate(X_train, y_train)
        
        # Get feature importance
        feature_importance = trainer.get_feature_importance()
        if not feature_importance.empty:
            logger.info("\nTop 10 Important Features:")
            logger.info(feature_importance.head(10).to_string(index=False))
        
        # Log to MLflow
        if config['training'].get('use_mlflow', False):
            mlflow.log_params(config['model']['hyperparameters'])
            mlflow.log_metrics(metrics)
            mlflow.log_metrics(cv_results)
            
            # Log model
            if config['model']['algorithm'] == 'xgboost':
                mlflow.xgboost.log_model(trainer.model, "model")
            elif config['model']['algorithm'] == 'lightgbm':
                mlflow.lightgbm.log_model(trainer.model, "model")
            else:
                mlflow.sklearn.log_model(trainer.model, "model")
        
        # Save model
        trainer.save_model(config['output']['model_path'])
        
        # Save metrics
        metrics_path = config['output']['metrics_path']
        Path(metrics_path).parent.mkdir(parents=True, exist_ok=True)
        
        all_metrics = {**metrics, **cv_results}
        with open(metrics_path, 'w') as f:
            json.dump(all_metrics, f, indent=2)
        
        logger.info(f"Metrics saved to {metrics_path}")
        logger.info("Training pipeline completed successfully!")
        
    finally:
        if config['training'].get('use_mlflow', False):
            mlflow.end_run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train attrition prediction model')
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    
    args = parser.parse_args()
    train_pipeline(args.config)
