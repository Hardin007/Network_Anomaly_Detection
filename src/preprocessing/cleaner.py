"""
Data Cleaning Utilities
Handles missing values, outliers, and data quality issues.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and prepare network traffic data."""
    
    def __init__(self):
        """Initialize data cleaner."""
        self.data = None
    
    def handle_missing_values(self, data: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """
        Handle missing values in data.
        
        Args:
            data: Input DataFrame
            strategy: 'drop', 'mean', 'median', 'forward_fill'
            
        Returns:
            Cleaned DataFrame
        """
        logger.info(f"Handling missing values with strategy: {strategy}")
        
        if strategy == 'drop':
            return data.dropna()
        elif strategy == 'mean':
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
        elif strategy == 'median':
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())
        elif strategy == 'forward_fill':
            data = data.fillna(method='ffill')
        
        logger.info(f"Missing values after cleaning: {data.isnull().sum().sum()}")
        return data
    
    def remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows.
        
        Args:
            data: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        before = len(data)
        data = data.drop_duplicates()
        after = len(data)
        logger.info(f"Removed {before - after} duplicate rows")
        return data
    
    def remove_outliers(self, data: pd.DataFrame, method: str = 'iqr', threshold: float = 3) -> pd.DataFrame:
        """
        Remove outliers from numeric columns.
        
        Args:
            data: Input DataFrame
            method: 'iqr' or 'zscore'
            threshold: Z-score threshold (for zscore method)
            
        Returns:
            DataFrame with outliers removed
        """
        logger.info(f"Removing outliers using {method} method")
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if method == 'iqr':
            for col in numeric_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                data = data[(data[col] >= Q1 - 1.5 * IQR) & (data[col] <= Q3 + 1.5 * IQR)]
        
        elif method == 'zscore':
            z_scores = np.abs((data[numeric_cols] - data[numeric_cols].mean()) / data[numeric_cols].std())
            data = data[(z_scores < threshold).all(axis=1)]
        
        logger.info(f"Data shape after outlier removal: {data.shape}")
        return data
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate data quality.
        
        Args:
            data: Input DataFrame
            
        Returns:
            True if data is valid, False otherwise
        """
        issues = []
        
        if data.empty:
            issues.append("Data is empty")
        
        if data.isnull().sum().any():
            issues.append(f"Found {data.isnull().sum().sum()} missing values")
        
        if len(data.duplicated()) > 0:
            issues.append(f"Found {len(data.duplicated())} duplicate rows")
        
        if issues:
            logger.warning("Data validation issues: " + "; ".join(issues))
            return False
        
        logger.info("Data validation passed")
        return True
    
    def clean(self, data: pd.DataFrame, steps: list = None) -> pd.DataFrame:
        """
        Execute full cleaning pipeline.
        
        Args:
            data: Input DataFrame
            steps: List of cleaning steps to apply
            
        Returns:
            Cleaned DataFrame
        """
        if steps is None:
            steps = ['handle_missing', 'remove_duplicates', 'remove_outliers', 'validate']
        
        for step in steps:
            if step == 'handle_missing':
                data = self.handle_missing_values(data)
            elif step == 'remove_duplicates':
                data = self.remove_duplicates(data)
            elif step == 'remove_outliers':
                data = self.remove_outliers(data)
            elif step == 'validate':
                self.validate_data(data)
        
        return data