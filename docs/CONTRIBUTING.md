# Contributing Guide

Thank you for your interest in contributing to Network Anomaly Detection!

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Commit: `git commit -am 'Add your feature'`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

## Development Workflow

### Setup Development Environment

```bash
git clone https://github.com/YOUR_USERNAME/Network_Anomaly_Detection.git
cd Network_Anomaly_Detection
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest black flake8
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting: `black src/`
- Use Flake8 for linting: `flake8 src/`

### Testing

Write tests for new features:

```bash
pytest tests/
pytest tests/ --cov=src  # With coverage
```

### Commit Messages

- Use clear, descriptive commit messages
- Format: `Type: Description` (e.g., `Feature: Add new model`, `Fix: Bug in preprocessing`)

## Types of Contributions

### Bug Reports

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs. actual behavior
- Error messages/traceback

### Feature Requests

- Clearly describe the feature
- Explain the use case
- Provide examples

### Code Contributions

- Ensure tests pass
- Add tests for new code
- Update documentation
- Follow code style guidelines

### Documentation

- Fix typos
- Clarify unclear sections
- Add examples
- Update API docs

## Pull Request Process

1. Update README.md if needed
2. Add tests for new features
3. Ensure tests pass: `pytest`
4. Run linting: `flake8 src/`
5. Format code: `black src/`
6. Write clear PR description

## Questions?

Feel free to open an issue or discussion.

Thank you for contributing! 🎉
