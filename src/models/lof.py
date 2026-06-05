"""
Local Outlier Factor (LOF) Anomaly Detector
Density-based method for anomaly detection.
"""

import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from .base import BaseAnomalyDetector
import logging

logger = logging.getLogger(__name__)


class LOFDetector(BaseAnomalyDetector):
    """Local Outlier Factor-based anomaly detector."""
    
    def __init__(self, n_neighbors: int = 20, contamination: str = 'auto',
                 algorithm: str = 'auto', metric: str = 'minkowski'):
        """
        Initialize LOF detector.
        
        Args:
            n_neighbors: Number of neighbors for density estimation
            contamination: Expected proportion of anomalies ('auto' or float)
            algorithm: Algorithm for neighbor search ('auto', 'ball_tree', 'kd_tree', 'brute')
            metric: Distance metric ('minkowski', 'euclidean', etc.)
        """
        super().__init__(name="LocalOutlierFactor")
        self.n_neighbors = n_neighbors
        self.contamination = contamination
        self.algorithm = algorithm
        self.metric = metric
        
        self.model = LocalOutlierFactor(
            n_neighbors=n_neighbors,
            contamination=contamination,
            algorithm=algorithm,
            metric=metric
        )
    
    def fit(self, X: np.ndarray) -> 'LOFDetector':
        """
        Fit LOF model.
        
        Args:
            X: Training feature matrix
            
        Returns:
            Self for method chaining
        """
        self.model.fit(X)
        self.is_fitted = True
        logger.info(f"LOF model fitted with n_neighbors={self.n_neighbors}")
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
        Get anomaly scores (LOF values).
        
        Args:
            X: Feature matrix to score
            
        Returns:
            Array of LOF scores (values > 1 indicate anomalies)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before scoring")
        
        return self.model.negative_outlier_factor_