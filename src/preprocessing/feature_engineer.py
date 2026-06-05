"""
Feature Engineering Utilities
Handles feature extraction and transformation.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Engineer and transform features for model training."""
    
    def __init__(self, scaling: str = 'standard'):
        """
        Initialize feature engineer.
        
        Args:
            scaling: 'standard' or 'minmax'
        """
        self.scaler = None
        self.scaling = scaling
        self.feature_selector = None
        self._init_scaler()
    
    def _init_scaler(self):
        """Initialize scaler based on configuration."""
        if self.scaling == 'standard':
            self.scaler = StandardScaler()
        elif self.scaling == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {self.scaling}")
    
    def scale_features(self, X: np.ndarray, fit: bool = True) -> np.ndarray:
        """
        Scale features using configured scaler.
        
        Args:
            X: Feature matrix
            fit: Whether to fit the scaler
            
        Returns:
            Scaled feature matrix
        """
        if fit:
            X_scaled = self.scaler.fit_transform(X)
            logger.info(f"Scaler fitted and features scaled using {self.scaling} scaling")
        else:
            X_scaled = self.scaler.transform(X)
            logger.info(f"Features scaled using {self.scaling} scaling")
        
        return X_scaled
    
    def select_features(self, X: np.ndarray, y: np.ndarray, k: int = 10, 
                       method: str = 'mutual_info') -> np.ndarray:
        """
        Select top k features using feature importance.
        
        Args:
            X: Feature matrix
            y: Target labels
            k: Number of features to select
            method: 'mutual_info' or 'f_classif'
            
        Returns:
            Transformed feature matrix with selected features
        """
        if method == 'mutual_info':
            selector = SelectKBest(mutual_info_classif, k=k)
        elif method == 'f_classif':
            selector = SelectKBest(f_classif, k=k)
        else:
            raise ValueError(f"Unknown feature selection method: {method}")
        
        X_selected = selector.fit_transform(X, y)
        self.feature_selector = selector
        
        logger.info(f"Selected top {k} features using {method}")
        return X_selected
    
    def get_feature_importance(self) -> dict:
        """
        Get feature importance scores.
        
        Returns:
            Dictionary mapping feature indices to importance scores
        """
        if self.feature_selector is None:
            logger.warning("Feature selector not fitted yet")
            return {}
        
        scores = self.feature_selector.scores_
        return {i: score for i, score in enumerate(scores)}
    
    def create_polynomial_features(self, X: np.ndarray, degree: int = 2) -> np.ndarray:
        """
        Create polynomial features.
        
        Args:
            X: Feature matrix
            degree: Polynomial degree
            
        Returns:
            Feature matrix with polynomial features
        """
        poly_features = []
        for i in range(X.shape[1]):
            for j in range(i, X.shape[1]):
                for d in range(2, degree + 1):
                    poly_features.append(X[:, i] ** d * X[:, j] ** (degree - d))
        
        if poly_features:
            X_poly = np.column_stack([X] + poly_features)
            logger.info(f"Created polynomial features. New shape: {X_poly.shape}")
            return X_poly
        return X
    
    def create_interaction_features(self, X: np.ndarray) -> np.ndarray:
        """
        Create interaction features between columns.
        
        Args:
            X: Feature matrix
            
        Returns:
            Feature matrix with interaction features
        """
        interaction_features = []
        for i in range(X.shape[1]):
            for j in range(i + 1, X.shape[1]):
                interaction_features.append(X[:, i] * X[:, j])
        
        if interaction_features:
            X_interaction = np.column_stack([X] + interaction_features)
            logger.info(f"Created interaction features. New shape: {X_interaction.shape}")
            return X_interaction
        return X