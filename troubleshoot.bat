@echo off
echo Twitter Scanner - Troubleshooting Guide
echo =====================================
echo.

echo 1. Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    echo Python is installed correctly
)

echo.
echo 2. Checking if we're in the right directory...
echo Current directory: %CD%
if not exist "app.py" (
    echo ERROR: app.py not found in current directory
    echo Please navigate to the twitter_scanner folder
    pause
    exit /b 1
) else (
    echo app.py found
)

echo.
echo 3. Checking Python dependencies...
pip show flask
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Try running: pip install --upgrade pip
        echo Then run: pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo Dependencies are installed
)

echo.
echo 4. Testing the application...
echo Starting Twitter Scanner...
echo If you see any error messages, please note them down
echo.
python app.py

pause

