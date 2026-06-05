"""
Base Anomaly Detection Model
Defines interface for all anomaly detection models.
"""

from abc import ABC, abstractmethod
import numpy as np
import logging

logger = logging.getLogger(__name__)


class BaseAnomalyDetector(ABC):
    """Abstract base class for anomaly detectors."""
    
    def __init__(self, name: str = "BaseDetector"):
        """
        Initialize base detector.
        
        Args:
            name: Name of the detector
        """
        self.name = name
        self.model = None
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, X: np.ndarray) -> 'BaseAnomalyDetector':
        """
        Fit the model on training data.
        
        Args:
            X: Training feature matrix
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies.
        
        Args:
            X: Feature matrix to predict
            
        Returns:
            Array of predictions (1 for anomaly, -1 or 0 for normal)
        """
        pass
    
    @abstractmethod
    def predict_score(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores for samples.
        
        Args:
            X: Feature matrix to score
            
        Returns:
            Array of anomaly scores
        """
        pass
    
    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """
        Fit model and predict in one step.
        
        Args:
            X: Feature matrix
            
        Returns:
            Predictions
        """
        self.fit(X)
        return self.predict(X)
    
    def save(self, filepath: str):
        """
        Save model to file.
        
        Args:
            filepath: Path to save model
        """
        import joblib
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str):
        """
        Load model from file.
        
        Args:
            filepath: Path to load model from
        """
        import joblib
        self.model = joblib.load(filepath)
        self.is_fitted = True
        logger.info(f"Model loaded from {filepath}")