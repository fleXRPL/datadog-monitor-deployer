# Contributing to Datadog Monitor Deployer

First off, thank you for considering contributing to Datadog Monitor Deployer! It's people like you that make it such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include any error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fork the repo and create your branch from `main`
* If you've added code that should be tested, add tests
* If you've changed APIs, update the documentation
* Ensure the test suite passes
* Make sure your code lints
* Issue that pull request!

## Development Process

1. Clone the repository
```bash
git clone https://github.com/fleXRPL/datadog-monitor-deployer.git
cd datadog-monitor-deployer
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

4. Make your changes
* Write meaningful commit messages
* Add tests for new functionality
* Update documentation as needed

5. Run the test suite
```bash
pytest
```

6. Check code style
```bash
black src tests
flake8 src tests
mypy src tests
```

7. Create a pull request

## Style Guide

* Follow PEP 8 style guide
* Use [Black](https://github.com/psf/black) for code formatting
* Write docstrings for all public modules, functions, classes, and methods
* Use type hints for function arguments and return values
* Keep functions focused and concise
* Write clear commit messages

## Documentation

* Keep README.md up to date
* Update docstrings for any modified code
* Add examples for new features
* Update CHANGELOG.md with notable changes

## Testing

* Write unit tests for new functionality
* Ensure all tests pass before submitting PR
* Maintain or improve code coverage
* Include both positive and negative test cases

## Questions?

Feel free to open an issue with your question or reach out to the maintainers directly.

Thank you for your contribution! 🎉 