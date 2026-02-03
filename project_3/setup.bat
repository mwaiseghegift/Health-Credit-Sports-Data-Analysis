@echo off
REM Setup script for Real-Time Sports Analytics (Windows)
REM This script automates the initial setup process

echo ======================================================
echo  Real-Time Sports Analytics - Setup Script
echo ======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python 3 is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo  Python detected
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo  Creating virtual environment...
    python -m venv venv
    echo  Virtual environment created
) else (
    echo  Virtual environment already exists
)
echo.

REM Activate virtual environment
echo  Activating virtual environment...
call venv\Scripts\activate.bat
echo  Virtual environment activated
echo.

REM Install dependencies
echo  Installing dependencies...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
echo  Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo  Creating .env file...
    copy .env.example .env
    echo  .env file created
    echo.
    echo   IMPORTANT: Edit .env file and add your Football-Data.org API key
    echo    Get your free API key: https://www.football-data.org/client/register
    echo.
) else (
    echo  .env file already exists
    echo.
)

REM Initialize database
echo  Initializing database...
python -c "from src.db_utils import get_database_manager; db = get_database_manager(); db.close()"
echo  Database initialized
echo.

REM Run system tests
echo  Running system tests...
python test_system.py
echo.

echo ======================================================
echo  Setup Complete!
echo ======================================================
echo.
echo  Next steps:
echo    1. Edit .env file and add your API key
echo    2. Run: python src\fetch_data.py (to fetch data)
echo    3. Run: streamlit run src\app.py (to launch dashboard)
echo.
echo Or run with scheduler:
echo    python src\scheduler.py
echo.
echo ======================================================
pause
