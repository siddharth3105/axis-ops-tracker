# push_to_github.ps1
# Run this once to authenticate with GitHub and push the repo.
# Usage: Right-click -> Run with PowerShell

$env:PATH += ";C:\Program Files\GitHub CLI;C:\Program Files\Git\bin;C:\Program Files\Git\cmd"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AXIS OPS TRACKER - Push to GitHub" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Authenticate
Write-Host "[1/3] Logging into GitHub..." -ForegroundColor Green
Write-Host "      A browser window will open. Paste the code shown and click Authorize." -ForegroundColor Yellow
Write-Host ""
gh auth login --hostname github.com --git-protocol https --web

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Authentication failed. Try running: gh auth login" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/3] Creating GitHub repository..." -ForegroundColor Green
gh repo create axis-ops-tracker --public --description "Employee tracking dashboard for Axis Ops - Flask + SQLite + Google Sheets integration" --confirm 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "      Repo may already exist, continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Pushing code to GitHub..." -ForegroundColor Green

Set-Location "C:\Users\SPURGE\AXIS AI TRACKER"

# Update remote to use gh-authenticated URL
git remote set-url origin "https://github.com/siddharth3105/axis-ops-tracker.git"
git push -u origin master

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Repo is live at:" -ForegroundColor Green
    Write-Host "  https://github.com/siddharth3105/axis-ops-tracker" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Push failed. Check error above." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to close"
