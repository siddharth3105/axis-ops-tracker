####################################################################
#  AXIS OPS TRACKER - Token-Based GitHub Push (no browser needed)
#
#  HOW TO GET A TOKEN (2 minutes):
#  1. Go to: https://github.com/settings/tokens/new
#  2. Note: "axis-ops-tracker deploy"
#  3. Expiration: 90 days
#  4. Scopes: check [x] repo
#  5. Click "Generate token"
#  6. COPY the token (starts with ghp_...)
#  7. Paste it below where it says YOUR_TOKEN_HERE
#  8. Right-click this file -> Run with PowerShell
####################################################################

# ── PASTE YOUR TOKEN HERE ────────────────────────────────────────
$TOKEN = "YOUR_TOKEN_HERE"
# ────────────────────────────────────────────────────────────────

$OWNER   = "siddharth3105"
$REPO    = "axis-ops-tracker"
$PROJECT = "C:\Users\SPURGE\AXIS AI TRACKER"

$env:PATH += ";C:\Program Files\Git\bin;C:\Program Files\Git\cmd"

if ($TOKEN -eq "YOUR_TOKEN_HERE") {
    Write-Host ""
    Write-Host "ERROR: You need to paste your GitHub token into this script first!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Get one at: https://github.com/settings/tokens/new" -ForegroundColor Cyan
    Write-Host "  - Check [x] repo scope" -ForegroundColor Gray
    Write-Host "  - Copy the token (ghp_...)" -ForegroundColor Gray
    Write-Host "  - Edit this file and replace YOUR_TOKEN_HERE" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Axis Ops Tracker -> GitHub Push" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan

# ── Create repo via API ──────────────────────────────────────────
Write-Host "`n[1/2] Creating GitHub repo..." -ForegroundColor Green

$headers = @{
    Authorization = "token $TOKEN"
    Accept        = "application/vnd.github.v3+json"
    "User-Agent"  = "AxisOpsTracker"
}

$body = @{
    name        = $REPO
    description = "Axis Ops employee tracker: Flask + SQLite + Google Sheets integration"
    private     = $false
    auto_init   = $false
} | ConvertTo-Json

try {
    $resp = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method POST -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "      Repo created: $($resp.html_url)" -ForegroundColor Green
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 422) {
        Write-Host "      Repo already exists, continuing..." -ForegroundColor Yellow
    } else {
        Write-Host "      API error: $_" -ForegroundColor Red
        Read-Host "Press Enter to exit"; exit 1
    }
}

# ── Push via HTTPS with token ────────────────────────────────────
Write-Host "`n[2/2] Pushing code..." -ForegroundColor Green

Set-Location $PROJECT

# Embed token in URL so git doesn't ask for password
$remoteUrl = "https://${OWNER}:${TOKEN}@github.com/$OWNER/$REPO.git"
git remote set-url origin $remoteUrl
git push -u origin master

if ($LASTEXITCODE -eq 0) {
    # Remove token from remote URL after push (security)
    git remote set-url origin "https://github.com/$OWNER/$REPO.git"

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  PUSHED! Repo is live at:" -ForegroundColor Green
    Write-Host "  https://github.com/$OWNER/$REPO" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Green
} else {
    Write-Host "Push failed. Check your token has 'repo' scope." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to close"
