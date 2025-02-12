#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# Datadog API credentials
DD_API_KEY=your-api-key-here
DD_APP_KEY=your-app-key-here

# Environment (development/production)
DD_ENV=development
EOL
    echo ".env file created. Please update with your Datadog credentials."
fi

echo "Development environment setup complete!"
echo "Remember to:"
echo "1. Update .env with your Datadog credentials"
echo "2. Run 'source venv/bin/activate' to activate the virtual environment"
echo "3. Run 'pytest' to verify the setup" 