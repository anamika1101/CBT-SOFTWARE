@echo off
REM CBT Software - Run script for Windows
echo ========================================
echo   CBT Online Examination Portal
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+ and add it to PATH.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install -r requirements.txt -q

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Starting development server...
echo.
echo   Open: http://127.0.0.1:8000
echo   Press Ctrl+C to stop
echo.
python manage.py runserver
