# Axis Ops Tracker - Quick Start Script for Windows PowerShell
# This script automates the setup and launch process

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      AXIS OPS TRACKER - Quick Start Script" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Green

# Try to find Python
$pythonCmd = $null
$pythonCommands = @("python", "python3", "py")

foreach ($cmd in $pythonCommands) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $result -match "Python") {
            $pythonCmd = $cmd
            Write-Host "   ✓ Python found: $result" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

if ($null -eq $pythonCmd) {
    Write-Host ""
    Write-Host "   ✗ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Please install Python 3.8+ first:" -ForegroundColor Yellow
    Write-Host "   1. Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "   2. Run installer and CHECK 'Add Python to PATH'" -ForegroundColor Cyan
    Write-Host "   3. Restart PowerShell and run this script again" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
Write-Host ""
Write-Host "[2/5] Checking virtual environment..." -ForegroundColor Green
if (Test-Path "venv") {
    Write-Host "   ✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "   → Creating virtual environment..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ✗ Failed to create virtual environment" -ForegroundColor Red
        Write-Host "   Try running: $pythonCmd -m pip install --upgrade pip" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "   ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Green
$activateScript = ".\venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "   ✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "   ✗ Cannot find activation script" -ForegroundColor Red
    Write-Host "   Virtual environment may be corrupted. Delete 'venv' folder and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Green
Write-Host "   → This may take a few minutes..." -ForegroundColor Yellow
& $pythonCmd -m pip install --upgrade pip setuptools wheel --quiet
& $pythonCmd -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ⚠ Some dependencies may have failed to install" -ForegroundColor Yellow
    Write-Host "   The app may still work. Continuing..." -ForegroundColor Yellow
} else {
    Write-Host "   ✓ Dependencies installed" -ForegroundColor Green
}

# Check if database exists
Write-Host ""
Write-Host "[5/5] Checking database..." -ForegroundColor Green
if (Test-Path "data\axis_ops.db") {
    Write-Host "   ✓ Database found" -ForegroundColor Green
} else {
    Write-Host "   → Database not found. Creating with sample data..." -ForegroundColor Yellow
    & $pythonCmd scripts\import_sample_data.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠ Sample data import had issues, but continuing..." -ForegroundColor Yellow
    }
}

# Display information
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "                 🚀 READY TO LAUNCH!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Dashboard will open at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📝 Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "Tip: If port 5000 is busy, edit run.py to use a different port" -ForegroundColor DarkGray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Start the application
& $pythonCmd run.py
