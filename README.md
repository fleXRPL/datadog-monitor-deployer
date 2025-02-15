# Datadog Monitor Deployer

#### versions

[![PyPI version](https://img.shields.io/pypi/v/datadog-monitor-deployer.svg)](https://pypi.org/project/datadog-monitor-deployer/)
[![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![CI/CD Pipeline](https://github.com/fleXRPL/datadog-monitor-deployer/actions/workflows/workflow.yml/badge.svg)](https://github.com/fleXRPL/datadog-monitor-deployer/actions/workflows/workflow.yml)
[![Python](https://img.shields.io/pypi/pyversions/datadog-monitor-deployer.svg)](https://pypi.org/project/datadog-monitor-deployer/)

#### health

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-monitor-deployer&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-monitor-deployer)
[![Overall Coverage](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-monitor-deployer&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-monitor-deployer)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-monitor-deployer&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-monitor-deployer)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-monitor-deployer&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-monitor-deployer)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-monitor-deployer&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-monitor-deployer)
[![Dependabot Status](https://img.shields.io/badge/Dependabot-enabled-success.svg)](https://github.com/fleXRPL/datadog-monitor-deployer/blob/main/.github/dependabot.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

#### stats

[![Downloads](https://pepy.tech/badge/datadog-monitor-deployer)](https://pepy.tech/project/datadog-monitor-deployer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful and flexible tool for managing Datadog monitors as code. This project enables teams to define, deploy, and manage Datadog monitors using a declarative approach, supporting both YAML/JSON configurations and Python classes.

## 🌟 Key Features

- 📝 Multiple Definition Formats:
  - YAML/JSON with schema validation
  - Python classes for programmatic creation
  - Hybrid approach supporting both methods
- 🔍 Comprehensive Monitor Type Support:
  - Metric monitors
  - Event monitors
  - Log monitors
  - APM monitors
  - Network monitors
  - Process monitors
- ⚡ Advanced Functionality:
  - Robust alerting configuration
  - Multiple notification channels (Email, Slack, PagerDuty)
  - Custom message templates
  - Tagging and organization
  - Full CRUD operations
- 🛡️ Enterprise-Ready:
  - Idempotent operations
  - Comprehensive testing
  - Secure authentication handling
  - CI/CD pipeline integration

## 🚀 Quick Start

1. Install the package:

```bash
pip install datadog-monitor-deployer
```

2. Set up your Datadog credentials:

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

3. Create a monitor definition (example.yaml):

```yaml
monitors:
  - name: "High CPU Usage Alert"
    type: "metric alert"
    query: "avg(last_5m):avg:system.cpu.user{*} > 80"
    message: "CPU usage is above 80%"
    tags:
      - "env:production"
      - "service:web"
    options:
      notify_no_data: true
      evaluation_delay: 900
```

4. Deploy your monitor:

```bash
dd-monitor deploy example.yaml
```

## 📚 Documentation

For detailed documentation, visit our [Documentation Site](https://github.com/fleXRPL/datadog-monitor-deployer/wiki).

- [Getting Started Guide](https://github.com/fleXRPL/datadog-monitor-deployer/wiki/Getting-Started)
- [Configuration Reference](https://github.com/fleXRPL/datadog-monitor-deployer/wiki/Configuration)
- [API Documentation](https://github.com/fleXRPL/datadog-monitor-deployer/wiki/API)
- [CLI Reference](https://github.com/fleXRPL/datadog-monitor-deployer/wiki/CLI)
- [Best Practices](https://github.com/fleXRPL/datadog-monitor-deployer/wiki/Best-Practices)

## 🛠️ Development Setup

1. Clone the repository:

```bash
git clone https://github.com/fleXRPL/datadog-monitor-deployer.git
cd datadog-monitor-deployer
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

4. Run tests:

```bash
pytest
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

Please review our [Security Policy](SECURITY.md) for reporting security vulnerabilities.

## 📊 Project Status

This project is actively maintained and used in production environments. For the latest updates, see our [Changelog](CHANGELOG.md).

---

Built with ❤️ by the fleXRPL team
