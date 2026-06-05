"""Test Evaluation Module"""

import pytest
import numpy as np
from src.evaluation import MetricsCalculator


class TestMetricsCalculator:
    """Test evaluation metrics calculation."""
    
    def test_calculate_metrics(self):
        """Test metrics calculation."""
        y_true = np.array([0, 0, 1, 1, 0, 1])
        y_pred = np.array([0, 0, 1, 0, 0, 1])
        y_score = np.array([0.1, 0.2, 0.8, 0.3, 0.15, 0.9])
        
        metrics = MetricsCalculator.calculate_metrics(y_true, y_pred, y_score)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert 'roc_auc' in metrics
        assert 'confusion_matrix' in metrics
        
        # Check value ranges
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['precision'] <= 1
        assert 0 <= metrics['recall'] <= 1
        assert 0 <= metrics['f1_score'] <= 1
    
    def test_calculate_metrics_with_anomaly_labels(self):
        """Test metrics with -1/1 labels (anomaly format)."""
        y_true = np.array([-1, -1, 1, 1, -1, 1])
        y_pred = np.array([-1, -1, 1, -1, -1, 1])
        
        metrics = MetricsCalculator.calculate_metrics(y_true, y_pred)
        
        assert 'accuracy' in metrics
        assert 0 <= metrics['accuracy'] <= 1
    
    def test_classification_report(self):
        """Test classification report generation."""
        y_true = np.array([0, 0, 1, 1, 0, 1])
        y_pred = np.array([0, 0, 1, 0, 0, 1])
        
        report = MetricsCalculator.get_classification_report(y_true, y_pred)
        
        assert isinstance(report, str)
        assert 'Normal' in report or 'normal' in report.lower()
        assert 'Anomaly' in report or 'anomaly' in report.lower()
