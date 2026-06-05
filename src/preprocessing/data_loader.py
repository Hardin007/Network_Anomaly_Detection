"""
Data Loading Utilities
Handles loading and parsing network traffic data.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and initialize network traffic data."""
    
    def __init__(self):
        """Initialize data loader."""
        self.data = None
        self.features = None
        self.labels = None
    
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with loaded data
        """
        try:
            self.data = pd.read_csv(filepath)
            logger.info(f"Loaded data from {filepath}. Shape: {self.data.shape}")
            return self.data
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            raise
    
    def get_feature_matrix(self) -> np.ndarray:
        """
        Get feature matrix (X).
        
        Returns:
            Feature matrix
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_csv first.")
        
        # Exclude label column if it exists
        if 'label' in self.data.columns:
            return self.data.drop('label', axis=1).values
        return self.data.values
    
    def get_labels(self) -> Optional[np.ndarray]:
        """
        Get labels (y) if available.
        
        Returns:
            Label array or None if not available
        """
        if self.data is None:
            return None
        
        if 'label' in self.data.columns:
            return self.data['label'].values
        return None
    
    def split_features_labels(self) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Split data into features and labels.
        
        Returns:
            Tuple of (features, labels)
        """
        return self.get_feature_matrix(), self.get_labels()
    
    def get_feature_names(self) -> list:
        """
        Get feature column names.
        
        Returns:
            List of feature names
        """
        if self.data is None:
            return []
        
        feature_cols = [col for col in self.data.columns if col != 'label']
        return feature_cols
    
    def info(self):
        """Print data information."""
        if self.data is not None:
            self.data.info()
            print("\nBasic Statistics:")
            print(self.data.describe())