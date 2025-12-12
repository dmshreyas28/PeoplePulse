"""Model evaluation module."""
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, roc_curve,
    precision_recall_curve, confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate trained models."""
    
    def __init__(self, model_path: str):
        """Load model from disk.
        
        Args:
            model_path: Path to saved model
        """
        logger.info(f"Loading model from {model_path}")
        artifacts = joblib.load(model_path)
        
        self.model = artifacts['model']
        self.preprocessor = artifacts['preprocessor']
        self.feature_names = artifacts.get('feature_names', [])
        self.config = artifacts.get('config', {})
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """Comprehensive model evaluation.
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        logger.info("Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        return metrics
    
    def plot_roc_curve(
        self, 
        X_test: np.ndarray, 
        y_test: np.ndarray,
        save_path: str = None
    ):
        """Plot ROC curve.
        
        Args:
            X_test: Test features
            y_test: Test labels
            save_path: Path to save plot
        """
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"ROC curve saved to {save_path}")
        
        plt.show()
    
    def plot_confusion_matrix(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        save_path: str = None
    ):
        """Plot confusion matrix.
        
        Args:
            X_test: Test features
            y_test: Test labels
            save_path: Path to save plot
        """
        y_pred = self.model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Attrition', 'Attrition'],
            yticklabels=['No Attrition', 'Attrition']
        )
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Confusion Matrix')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Confusion matrix saved to {save_path}")
        
        plt.show()
    
    def plot_feature_importance(
        self,
        top_n: int = 15,
        save_path: str = None
    ):
        """Plot feature importance.
        
        Args:
            top_n: Number of top features to show
            save_path: Path to save plot
        """
        if not hasattr(self.model, 'feature_importances_'):
            logger.warning("Model doesn't have feature_importances_ attribute")
            return
        
        importance = self.model.feature_importances_
        indices = np.argsort(importance)[-top_n:]
        
        plt.figure(figsize=(10, 8))
        plt.barh(range(len(indices)), importance[indices])
        plt.yticks(range(len(indices)), [self.feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title(f'Top {top_n} Important Features')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Feature importance plot saved to {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Example usage
    evaluator = ModelEvaluator("./models/model.pkl")
    
    # Load test data
    # X_test, y_test = ... (load your test data)
    
    # metrics = evaluator.evaluate(X_test, y_test)
    # print(metrics)
    
    # evaluator.plot_roc_curve(X_test, y_test, save_path="./plots/roc_curve.png")
    # evaluator.plot_confusion_matrix(X_test, y_test, save_path="./plots/confusion_matrix.png")
    # evaluator.plot_feature_importance(save_path="./plots/feature_importance.png")
