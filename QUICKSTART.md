# Quick Start Guide

Get up and running with Network Anomaly Detection in 5 minutes!

## Installation

```bash
# Clone repository
git clone https://github.com/Hardin007/Network_Anomaly_Detection.git
cd Network_Anomaly_Detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Using the Pipeline Script

```bash
python src/main.py --config config/default_config.yaml --data data/your_data.csv
```

### 2. Using Python Code

```python
import numpy as np
from src.models import IsolationForestDetector
from src.preprocessing import DataLoader, FeatureEngineer
from src.evaluation import MetricsCalculator

# Load data
loader = DataLoader()
data = loader.load_csv('data/network_traffic.csv')
X, y = loader.split_features_labels()

# Preprocess features
engineer = FeatureEngineer(scaling='standard')
X_scaled = engineer.scale_features(X, fit=True)

# Train model
model = IsolationForestDetector(contamination=0.1)
model.fit(X_scaled)

# Get predictions
predictions = model.predict(X_scaled)
scores = model.predict_score(X_scaled)

# Evaluate
metrics = MetricsCalculator.calculate_metrics(y, predictions, scores)
print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"F1-Score: {metrics['f1_score']:.4f}")
```

## Available Models

1. **IsolationForestDetector** - Fast, tree-based approach
2. **LOFDetector** - Density-based method
3. **EnsembleDetector** - Combines multiple models

## Configuration

Edit `config/default_config.yaml` to customize:
- Data paths
- Model parameters
- Feature scaling
- Evaluation metrics

## Example with Different Models

```python
# Isolation Forest
from src.models import IsolationForestDetector
model = IsolationForestDetector(contamination=0.1, n_estimators=100)

# Local Outlier Factor
from src.models import LOFDetector
model = LOFDetector(n_neighbors=20)

# Ensemble
from src.models import EnsembleDetector
model = EnsembleDetector(models=['isolation_forest', 'lof'], voting='hard')
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full API reference
- Explore [notebooks/](notebooks/) for Jupyter examples
- See [CONTRIBUTING.md](docs/CONTRIBUTING.md) to contribute

## Common Issues

**Q: ImportError when running script?**
A: Make sure you've installed dependencies: `pip install -r requirements.txt`

**Q: Configuration file not found?**
A: Verify the config path is correct relative to where you're running the script.

**Q: Data format error?**
A: Ensure your CSV has columns: timestamp, src_ip, dst_ip, src_port, dst_port, protocol, bytes_sent, bytes_received, duration, packet_count, label

## Support

For issues or questions:
1. Check [GitHub Issues](https://github.com/Hardin007/Network_Anomaly_Detection/issues)
2. Read the [documentation](docs/)
3. Create a new issue with details
