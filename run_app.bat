@echo off
title Axis Ops Tracker

echo.
echo  ============================================
echo   AXIS OPS TRACKER - Starting...
echo  ============================================
echo.

cd /d "%~dp0"

REM Check venv exists
if not exist "venv\Scripts\python.exe" (
    echo  ERROR: Virtual environment not found.
    echo  Run setup first: python -m venv venv
    echo  Then: venv\Scripts\pip install -r requirements_core.txt
    pause
    exit /b 1
)

REM Check database exists, seed if not
if not exist "data\axis_ops.db" (
    echo  Seeding database with sample data...
    venv\Scripts\python.exe seed.py
    echo.
)

echo  Dashboard: http://localhost:5000
echo  Press CTRL+C to stop.
echo.

REM Open browser after 2 seconds
start "" timeout /t 2 >nul & start "" "http://localhost:5000"

REM Start Flask
venv\Scripts\python.exe run.py

pause
