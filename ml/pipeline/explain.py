"""SHAP explainability module."""
import shap
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainabilityService:
    """Generate model explanations using SHAP."""
    
    def __init__(self, model_path: str):
        """Load model and initialize SHAP explainer.
        
        Args:
            model_path: Path to saved model
        """
        logger.info(f"Loading model from {model_path}")
        artifacts = joblib.load(model_path)
        
        self.model = artifacts['model']
        self.preprocessor = artifacts['preprocessor']
        self.feature_names = artifacts.get('feature_names', [])
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)
        logger.info("SHAP explainer initialized")
    
    def explain_instance(
        self,
        X: np.ndarray,
        feature_names: list = None
    ) -> shap.Explanation:
        """Generate SHAP explanation for a single instance.
        
        Args:
            X: Feature array (single sample)
            feature_names: Optional feature names
            
        Returns:
            SHAP explanation object
        """
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Use positive class
        
        return shap_values
    
    def plot_waterfall(
        self,
        X: np.ndarray,
        idx: int = 0,
        save_path: str = None
    ):
        """Plot SHAP waterfall plot for a single prediction.
        
        Args:
            X: Feature array
            idx: Index of instance to explain
            save_path: Path to save plot
        """
        shap_values = self.explainer(X)
        
        if isinstance(shap_values.values, list):
            shap_values.values = shap_values.values[1]
        
        shap.plots.waterfall(shap_values[idx], show=False)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Waterfall plot saved to {save_path}")
        
        plt.show()
    
    def plot_force(
        self,
        X: np.ndarray,
        idx: int = 0,
        save_path: str = None
    ):
        """Plot SHAP force plot.
        
        Args:
            X: Feature array
            idx: Index of instance to explain
            save_path: Path to save plot
        """
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        shap.force_plot(
            self.explainer.expected_value[1] if isinstance(self.explainer.expected_value, list) 
            else self.explainer.expected_value,
            shap_values[idx],
            X[idx],
            feature_names=self.feature_names,
            matplotlib=True,
            show=False
        )
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Force plot saved to {save_path}")
        
        plt.show()
    
    def plot_summary(
        self,
        X: np.ndarray,
        plot_type: str = "bar",
        save_path: str = None
    ):
        """Plot SHAP summary plot.
        
        Args:
            X: Feature array
            plot_type: Type of plot ('bar' or 'dot')
            save_path: Path to save plot
        """
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        plt.figure(figsize=(10, 8))
        shap.summary_plot(
            shap_values,
            X,
            feature_names=self.feature_names,
            plot_type=plot_type,
            show=False
        )
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Summary plot saved to {save_path}")
        
        plt.show()
    
    def get_top_features(
        self,
        X: np.ndarray,
        idx: int = 0,
        top_n: int = 5
    ) -> pd.DataFrame:
        """Get top contributing features for a prediction.
        
        Args:
            X: Feature array
            idx: Index of instance
            top_n: Number of top features
            
        Returns:
            DataFrame with top features and their SHAP values
        """
        shap_values = self.explainer.shap_values(X)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        # Get feature contributions
        contributions = list(zip(
            self.feature_names,
            X[idx],
            shap_values[idx]
        ))
        
        # Sort by absolute SHAP value
        contributions.sort(key=lambda x: abs(x[2]), reverse=True)
        
        # Create DataFrame
        df = pd.DataFrame(
            contributions[:top_n],
            columns=['Feature', 'Value', 'SHAP_Value']
        )
        
        return df


if __name__ == "__main__":
    # Example usage
    explainer = ExplainabilityService("./models/model.pkl")
    
    # Load sample data
    # X = ... (load your data)
    
    # Generate explanations
    # explainer.plot_summary(X, save_path="./plots/shap_summary.png")
    # explainer.plot_waterfall(X, idx=0, save_path="./plots/shap_waterfall.png")
    # top_features = explainer.get_top_features(X, idx=0)
    # print(top_features)
