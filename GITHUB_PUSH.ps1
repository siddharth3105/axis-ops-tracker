####################################################################
#  AXIS OPS TRACKER - One-Shot GitHub Push
#  Run this ONCE in PowerShell to create the repo and push.
#  Right-click this file -> "Run with PowerShell"
####################################################################

$ErrorActionPreference = "Stop"
$PROJECT = "C:\Users\SPURGE\AXIS AI TRACKER"
$REPO    = "axis-ops-tracker"
$OWNER   = "siddharth3105"

$env:PATH += ";C:\Program Files\GitHub CLI;C:\Program Files\Git\bin;C:\Program Files\Git\cmd"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Axis Ops Tracker -> GitHub Push" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan

# ── Step 1: Authenticate ────────────────────────────────────────
Write-Host "`n[1/3] GitHub Login" -ForegroundColor Green
Write-Host "      Your browser will open. Log in and click Authorize." -ForegroundColor Gray

gh auth login `
    --hostname github.com `
    --git-protocol https `
    --web

Write-Host "      Logged in." -ForegroundColor Green

# ── Step 2: Create repo ──────────────────────────────────────────
Write-Host "`n[2/3] Creating repo: $OWNER/$REPO" -ForegroundColor Green

$existing = gh repo view "$OWNER/$REPO" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "      Repo already exists, skipping create." -ForegroundColor Yellow
} else {
    gh repo create "$REPO" `
        --public `
        --description "Axis Ops employee tracker: Flask + SQLite + Google Sheets integration" `
        --confirm
    Write-Host "      Repo created." -ForegroundColor Green
}

# ── Step 3: Push ─────────────────────────────────────────────────
Write-Host "`n[3/3] Pushing code..." -ForegroundColor Green
Set-Location $PROJECT

git remote set-url origin "https://github.com/$OWNER/$REPO.git"
git push -u origin master

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  DONE! Your repo is live at:" -ForegroundColor Green
Write-Host "  https://github.com/$OWNER/$REPO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to close"
