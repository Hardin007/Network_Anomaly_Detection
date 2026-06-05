# Jupyter Notebooks

This directory contains Jupyter notebooks for:

1. **01_exploratory_analysis.ipynb** - Data exploration and visualization
2. **02_model_development.ipynb** - Model training and comparison
3. **03_results_analysis.ipynb** - Results analysis and insights

## Running Notebooks

```bash
jupyter notebook
```

Or with JupyterLab:

```bash
jupyterlab
```

## Requirements

Install Jupyter:
```bash
pip install jupyter jupyterlab
```

## Example Usage

```python
from src.models import IsolationForestDetector
from src.preprocessing import DataLoader

# Load data
loader = DataLoader()
data = loader.load_csv('data/network_traffic.csv')
X, y = loader.split_features_labels()

# Train model
model = IsolationForestDetector()
model.fit(X)

# Get predictions
predictions = model.predict(X)
```
