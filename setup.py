from setuptools import setup, find_packages

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datadog-monitor-deployer",
    version="0.1.0",
    author="fleXRPL Team",
    author_email="contact@flexrpl.org",
    description="A powerful tool for managing Datadog monitors as code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fleXRPL/datadog-monitor-deployer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "dd-monitor=datadog_monitor_deployer.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)