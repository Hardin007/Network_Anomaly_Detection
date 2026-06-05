"""Test Models Module"""

import pytest
import numpy as np
from src.models import IsolationForestDetector, LOFDetector, EnsembleDetector


class TestIsolationForestDetector:
    """Test Isolation Forest detector."""
    
    def test_initialization(self):
        """Test detector initialization."""
        detector = IsolationForestDetector(contamination=0.1)
        assert detector.name == "IsolationForest"
        assert not detector.is_fitted
    
    def test_fit_and_predict(self):
        """Test model fitting and prediction."""
        X_train = np.random.rand(100, 5)
        X_test = np.random.rand(20, 5)
        
        detector = IsolationForestDetector(contamination=0.1)
        detector.fit(X_train)
        
        assert detector.is_fitted
        predictions = detector.predict(X_test)
        assert predictions.shape == (20,)
        assert all(p in [-1, 1] for p in predictions)
    
    def test_predict_without_fit(self):
        """Test prediction without fitting raises error."""
        detector = IsolationForestDetector()
        X = np.random.rand(10, 5)
        
        with pytest.raises(ValueError):
            detector.predict(X)
    
    def test_predict_score(self):
        """Test anomaly scoring."""
        X_train = np.random.rand(100, 5)
        X_test = np.random.rand(20, 5)
        
        detector = IsolationForestDetector()
        detector.fit(X_train)
        scores = detector.predict_score(X_test)
        
        assert scores.shape == (20,)
        assert isinstance(scores[0], (float, np.floating))


class TestLOFDetector:
    """Test Local Outlier Factor detector."""
    
    def test_initialization(self):
        """Test detector initialization."""
        detector = LOFDetector(n_neighbors=20)
        assert detector.name == "LocalOutlierFactor"
        assert not detector.is_fitted
    
    def test_fit_and_predict(self):
        """Test model fitting and prediction."""
        X_train = np.random.rand(100, 5)
        X_test = np.random.rand(20, 5)
        
        detector = LOFDetector()
        detector.fit(X_train)
        
        assert detector.is_fitted
        predictions = detector.predict(X_test)
        assert predictions.shape == (20,)


class TestEnsembleDetector:
    """Test Ensemble detector."""
    
    def test_initialization(self):
        """Test ensemble initialization."""
        detector = EnsembleDetector(models=['isolation_forest', 'lof'])
        assert detector.name == "Ensemble"
        assert len(detector.models) == 2
    
    def test_fit_and_predict(self):
        """Test ensemble fitting and prediction."""
        X_train = np.random.rand(100, 5)
        X_test = np.random.rand(20, 5)
        
        detector = EnsembleDetector()
        detector.fit(X_train)
        
        assert detector.is_fitted
        predictions = detector.predict(X_test)
        assert predictions.shape == (20,)
