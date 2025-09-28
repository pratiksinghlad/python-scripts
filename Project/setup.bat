@echo off
REM Background Job Scheduler - Windows Setup Script
REM This script sets up the development environment on Windows

echo.
echo ====================================
echo Background Job Scheduler Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13+ from https://python.org
    pause
    exit /b 1
)

echo Found Python:
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installing package in development mode...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install package
    pause
    exit /b 1
)

echo.
echo Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
    echo Please edit .env file with your database credentials
) else (
    echo .env file already exists
)

echo.
echo Running tests...
pytest tests/ -v
if errorlevel 1 (
    echo WARNING: Some tests failed, but setup continues...
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Set up MySQL database (see SETUP.md)
echo 3. Run migrations: python -m background_job_scheduler.cli migrate
echo 4. Start scheduler: python run_scheduler.py
echo.
echo For detailed instructions, see SETUP.md
echo.
pause