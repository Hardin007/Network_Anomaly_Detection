"""
Isolation Forest Anomaly Detector
Fast, tree-based method for anomaly detection.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from .base import BaseAnomalyDetector
import logging

logger = logging.getLogger(__name__)


class IsolationForestDetector(BaseAnomalyDetector):
    """Isolation Forest-based anomaly detector."""
    
    def __init__(self, contamination: float = 0.1, n_estimators: int = 100, 
                 random_state: int = 42, n_jobs: int = -1):
        """
        Initialize Isolation Forest detector.
        
        Args:
            contamination: Expected proportion of anomalies
            n_estimators: Number of trees
            random_state: Random seed
            n_jobs: Number of parallel jobs
        """
        super().__init__(name="IsolationForest")
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.n_jobs = n_jobs
        
        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=n_jobs
        )
    
    def fit(self, X: np.ndarray) -> 'IsolationForestDetector':
        """
        Fit Isolation Forest model.
        
        Args:
            X: Training feature matrix
            
        Returns:
            Self for method chaining
        """
        self.model.fit(X)
        self.is_fitted = True
        logger.info(f"IsolationForest model fitted with contamination={self.contamination}")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies.
        
        Args:
            X: Feature matrix to predict
            
        Returns:
            Array of predictions (1 for normal, -1 for anomaly)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        return self.model.predict(X)
    
    def predict_score(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores.
        
        Args:
            X: Feature matrix to score
            
        Returns:
            Array of anomaly scores (negative values indicate anomalies)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before scoring")
        
        return self.model.score_samples(X)