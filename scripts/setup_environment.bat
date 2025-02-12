@echo off
setlocal

echo Setting up development environment...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install development dependencies
echo Installing development dependencies...
pip install -r requirements-dev.txt

REM Install pre-commit hooks
echo Installing pre-commit hooks...
pre-commit install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    (
        echo # Datadog API credentials
        echo DD_API_KEY=your-api-key-here
        echo DD_APP_KEY=your-app-key-here
        echo.
        echo # Environment (development/production^)
        echo DD_ENV=development
    ) > .env
    echo .env file created. Please update with your Datadog credentials.
)

echo Development environment setup complete!
echo Remember to:
echo 1. Update .env with your Datadog credentials
echo 2. Run 'venv\Scripts\activate.bat' to activate the virtual environment
echo 3. Run 'pytest' to verify the setup

endlocal 