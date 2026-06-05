# Installation Guide

Complete guide to installing and setting up Network Anomaly Detection.

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Linux, macOS, or Windows
- **Memory**: Minimum 4GB RAM (8GB+ recommended for large datasets)
- **Disk Space**: At least 2GB free space

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hardin007/Network_Anomaly_Detection.git
cd Network_Anomaly_Detection
```

### 2. Create Virtual Environment (Recommended)

#### Using venv

```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

#### Using conda

```bash
conda create -n network-anomaly python=3.8
conda activate network-anomaly
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import numpy, pandas, sklearn; print('Installation successful!')"
```

## Development Setup

For development, install additional dependencies:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 jupyterlab
```

## Configuration

1. Copy the default configuration:

```bash
cp config/default_config.yaml config/my_config.yaml
```

2. Edit `config/my_config.yaml` with your settings

## Running Your First Model

```bash
# Using main script
python src/main.py --config config/default_config.yaml --data data/your_data.csv

# Using Python API
from src.models import IsolationForestDetector
from src.preprocessing import DataLoader

loader = DataLoader()
data = loader.load_csv('data/your_data.csv')
X, y = loader.split_features_labels()

model = IsolationForestDetector()
model.fit(X)
predictions = model.predict(X)
```

## Troubleshooting

### ImportError: No module named 'tensorflow'

```bash
pip install tensorflow>=2.6.0
```

### sklearn version issues

```bash
pip install --upgrade scikit-learn
```

### YAML parsing errors

```bash
pip install PyYAML>=5.4.0
```

## Next Steps

- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API usage
- Explore [notebooks/](../notebooks/) for examples
- Read [README.md](../README.md) for project overview
