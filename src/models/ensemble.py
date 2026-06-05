"""
Ensemble Anomaly Detector
Combines multiple anomaly detection models.
"""

import numpy as np
from .base import BaseAnomalyDetector
from .isolation_forest import IsolationForestDetector
from .lof import LOFDetector
import logging

logger = logging.getLogger(__name__)


class EnsembleDetector(BaseAnomalyDetector):
    """Ensemble-based anomaly detector combining multiple models."""
    
    def __init__(self, models: list = None, voting: str = 'hard', weights: list = None):
        """
        Initialize ensemble detector.
        
        Args:
            models: List of model names (['isolation_forest', 'lof'])
            voting: 'hard' or 'soft' voting
            weights: Weights for each model (None = equal weights)
        """
        super().__init__(name="Ensemble")
        
        if models is None:
            models = ['isolation_forest', 'lof']
        
        self.models = {}
        self.voting = voting
        
        # Initialize models
        for model_name in models:
            if model_name == 'isolation_forest':
                self.models['isolation_forest'] = IsolationForestDetector()
            elif model_name == 'lof':
                self.models['lof'] = LOFDetector()
        
        # Set weights
        if weights is None:
            weights = [1.0 / len(self.models)] * len(self.models)
        
        self.weights = dict(zip(self.models.keys(), weights))
    
    def fit(self, X: np.ndarray) -> 'EnsembleDetector':
        """
        Fit all models in the ensemble.
        
        Args:
            X: Training feature matrix
            
        Returns:
            Self for method chaining
        """
        for name, model in self.models.items():
            model.fit(X)
            logger.info(f"Fitted {name} in ensemble")
        
        self.is_fitted = True
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies using voting.
        
        Args:
            X: Feature matrix to predict
            
        Returns:
            Array of predictions (1 for normal, -1 for anomaly)
        """
        if not self.is_fitted:
            raise ValueError("Ensemble must be fitted before prediction")
        
        if self.voting == 'hard':
            return self._hard_voting(X)
        else:
            return self._soft_voting(X)
    
    def _hard_voting(self, X: np.ndarray) -> np.ndarray:
        """
        Hard voting (majority).
        
        Args:
            X: Feature matrix
            
        Returns:
            Predictions
        """
        predictions = []
        for name, model in self.models.items():
            pred = model.predict(X)
            predictions.append(pred)
        
        predictions = np.array(predictions)
        # Majority voting: -1 if more models predict -1
        return np.where(np.sum(predictions == -1, axis=0) > len(self.models) / 2, -1, 1)
    
    def _soft_voting(self, X: np.ndarray) -> np.ndarray:
        """
        Soft voting (average scores).
        
        Args:
            X: Feature matrix
            
        Returns:
            Predictions
        """
        scores = []
        for name, model in self.models.items():
            score = model.predict_score(X)
            weight = self.weights[name]
            scores.append(score * weight)
        
        avg_score = np.mean(scores, axis=0)
        return np.where(avg_score < 0, -1, 1)
    
    def predict_score(self, X: np.ndarray) -> np.ndarray:
        """
        Get ensemble anomaly scores.
        
        Args:
            X: Feature matrix to score
            
        Returns:
            Array of ensemble scores
        """
        if not self.is_fitted:
            raise ValueError("Ensemble must be fitted before scoring")
        
        scores = []
        for name, model in self.models.items():
            score = model.predict_score(X)
            weight = self.weights[name]
            scores.append(score * weight)
        
        return np.mean(scores, axis=0)