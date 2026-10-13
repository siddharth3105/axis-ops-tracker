@echo off
REM Axis Ops Tracker - Simple Start Script for Windows
REM This is a simpler alternative to quick_start.ps1

echo.
echo ============================================================
echo       AXIS OPS TRACKER - Start Script
echo ============================================================
echo.

REM Check for Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo    X Python not found!
        echo.
        echo    Please install Python 3.8+ from: https://www.python.org/downloads/
        echo    Make sure to check "Add Python to PATH" during installation
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
        echo    / Python found (using py command^)
    )
) else (
    set PYTHON_CMD=python
    echo    / Python found
)

REM Check for virtual environment
echo.
echo [2/5] Checking virtual environment...
if exist "venv\" (
    echo    / Virtual environment found
) else (
    echo    ^ Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo    X Failed to create virtual environment
        pause
        exit /b 1
    )
    echo    / Virtual environment created
)

REM Activate virtual environment and install packages
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo    X Failed to activate virtual environment
    pause
    exit /b 1
)
echo    / Virtual environment activated

REM Install dependencies
echo.
echo [4/5] Installing dependencies...
echo    ^ This may take a few minutes...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo    ! Some packages may have failed, continuing...
) else (
    echo    / Dependencies installed
)

REM Check database
echo.
echo [5/5] Checking database...
if exist "data\axis_ops.db" (
    echo    / Database found
) else (
    echo    ^ Creating database with sample data...
    %PYTHON_CMD% scripts\import_sample_data.py
)

REM Start application
echo.
echo ============================================================
echo                  READY TO LAUNCH!
echo ============================================================
echo.
echo Starting Flask server...
echo.
echo Dashboard: http://localhost:5000
echo Press CTRL+C to stop the server
echo.
echo ============================================================
echo.

%PYTHON_CMD% run.py

pause
