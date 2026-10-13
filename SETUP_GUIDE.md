# 🚀 Axis Ops Tracker - Complete Setup Guide

This guide will walk you through setting up both the **Python Flask Dashboard** and **Google Sheets Integration**.

---

## 📋 Table of Contents

1. [Python Flask Dashboard Setup](#1-python-flask-dashboard-setup)
2. [Google Sheets Integration Setup](#2-google-sheets-integration-setup)
3. [Google Apps Script Setup](#3-google-apps-script-setup)
4. [Testing & Verification](#4-testing--verification)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Python Flask Dashboard Setup

### Step 1.1: Install Python

**Windows:**
1. Download Python 3.8+ from [python.org](https://python.org)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

**macOS/Linux:**
```bash
# macOS (using Homebrew)
brew install python3

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip
```

### Step 1.2: Setup Project

1. **Open terminal/PowerShell in project folder:**
   ```bash
   cd "C:\Users\SPURGE\AXIS AI TRACKER"
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 1.3: Import Sample Data (Optional)

```bash
python scripts/import_sample_data.py
```

This creates 30 sample employees with:
- Performance metrics
- Payment records
- Attendance data

### Step 1.4: Run the Application

```bash
python run.py
```

You should see:
```
🚀 AXIS OPS TRACKER - Starting Server
📊 Dashboard will be available at: http://localhost:5000
```

### Step 1.5: Open Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

You should see the dashboard with charts and statistics!

---

## 2. Google Sheets Integration Setup

### Step 2.1: Create Google Cloud Project

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create New Project:**
   - Click "Select a project" → "NEW PROJECT"
   - Name: "Axis Ops Tracker"
   - Click "CREATE"

3. **Enable APIs:**
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search and enable:
     - ✅ Google Sheets API
     - ✅ Google Drive API

### Step 2.2: Create Service Account

1. **Create Service Account:**
   - Go to "APIs & Services" → "Credentials"
   - Click "CREATE CREDENTIALS" → "Service Account"
   - Name: "axis-ops-tracker"
   - Click "CREATE AND CONTINUE"
   - Skip optional steps
   - Click "DONE"

2. **Generate Key:**
   - Click on the created service account
   - Go to "KEYS" tab
   - Click "ADD KEY" → "Create new key"
   - Choose "JSON"
   - Click "CREATE"
   - File will download (e.g., `axis-ops-tracker-xxxxx.json`)

3. **Save Credentials:**
   - Rename downloaded file to `credentials.json`
   - Move to: `config/credentials.json`

### Step 2.3: Configure Google Sheet

1. **Open your Google Sheet:**
   - URL: https://docs.google.com/spreadsheets/d/1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw/edit

2. **Share with Service Account:**
   - Click "Share" button
   - Open `config/credentials.json`
   - Find `"client_email"` value (e.g., `axis-ops-tracker@....iam.gserviceaccount.com`)
   - Paste this email in "Add people and groups"
   - Change permission to "Editor"
   - Uncheck "Notify people"
   - Click "Share"

3. **Copy Spreadsheet ID:**
   - From URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the `SPREADSHEET_ID` part

### Step 2.4: Update Configuration

Edit `scripts/google_sheets_integration.py`:

```python
# Line ~95, update with your spreadsheet ID:
SPREADSHEET_ID = '1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw'
```

### Step 2.5: Run Sync Script

```bash
python scripts/google_sheets_integration.py
```

Expected output:
```
============================================================
AXIS OPS TRACKER - GOOGLE SHEETS SYNC
============================================================
✓ Connected to Google Sheets
✓ Fetched XX records from Google Sheets
✓ Sync completed: XX new, XX updated
```

---

## 3. Google Apps Script Setup

### Step 3.1: Open Apps Script Editor

1. **Open your Google Sheet**
2. **Go to: Extensions > Apps Script**
3. **Delete any existing code**

### Step 3.2: Copy Script

1. **Open file:** `scripts/GoogleAppsScript.gs`
2. **Copy all content** (Ctrl+A, Ctrl+C)
3. **Paste in Apps Script editor**
4. **Save** (Ctrl+S or File > Save)
5. **Name project:** "Axis Ops Tracker"

### Step 3.3: Authorize Script

1. **Click "Run" button** (or F5)
2. **Choose function:** `onOpen`
3. **Click "Run"**
4. **Review Permissions:**
   - Click "Review permissions"
   - Choose your Google account
   - Click "Advanced"
   - Click "Go to Axis Ops Tracker (unsafe)"
   - Click "Allow"

### Step 3.4: Setup Triggers (Optional)

In Google Sheets, go to:
```
🔄 Axis Ops Tracker > Setup Triggers
```

This enables:
- ✅ Auto-validation on cell edit
- ✅ Daily metrics calculation at 2 AM
- ✅ Automatic backups every 6 hours

### Step 3.5: Test Features

Try these menu options:
- **📊 Sync to Dashboard** - Push data to Flask app
- **✅ Validate Data** - Check for errors
- **📈 Calculate Metrics** - Auto-calculate days worked

---

## 4. Testing & Verification

### Test 1: Dashboard Access

```bash
python run.py
```

Visit: `http://localhost:5000`

**Expected:**
- ✅ Dashboard loads
- ✅ Statistics show numbers
- ✅ Charts display

### Test 2: Employee Management

1. Go to **Employees** page
2. Click **+ Add Employee**
3. Fill form and save
4. Verify employee appears in list

### Test 3: Google Sheets Sync

1. Add a new row to Google Sheet
2. Run sync:
   ```bash
   python scripts/google_sheets_integration.py
   ```
3. Refresh dashboard
4. Verify new employee appears

### Test 4: Reports

1. Go to **Reports** page
2. Click **Generate** on any report
3. Verify CSV downloads

### Test 5: Analytics

1. Go to **Analytics** page
2. Verify charts display
3. Check performance rankings

---

## 5. Troubleshooting

### Problem: Module not found

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Problem: Cannot connect to Google Sheets

**Checklist:**
- ✅ `credentials.json` exists in `config/` folder
- ✅ APIs enabled in Google Cloud Console
- ✅ Service account has editor access to sheet
- ✅ Spreadsheet ID is correct

**Test connection:**
```python
python -c "import gspread; from oauth2client.service_account import ServiceAccountCredentials; creds = ServiceAccountCredentials.from_json_keyfile_name('config/credentials.json', ['https://spreadsheets.google.com/feeds']); client = gspread.authorize(creds); print('✓ Connected successfully!')"
```

### Problem: Database errors

**Solution - Reset database:**
```bash
# Delete database
rm data/axis_ops.db

# Reimport sample data
python scripts/import_sample_data.py

# Restart server
python run.py
```

### Problem: Port 5000 already in use

**Solution - Use different port:**

Edit `run.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

Or kill the process using port 5000:

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

### Problem: Virtual environment issues

**Solution - Recreate environment:**
```bash
# Remove old environment
rm -rf venv

# Create new
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux

# Install
pip install -r requirements.txt
```

### Problem: Google Apps Script not working

**Checklist:**
- ✅ Script is saved
- ✅ Project is authorized
- ✅ Sheet name matches CONFIG.EMPLOYEE_SHEET
- ✅ Check "View > Execution log" for errors

---

## 🎉 Success Checklist

- [ ] Python Flask dashboard runs successfully
- [ ] Can add/edit/delete employees
- [ ] Can view analytics and charts
- [ ] Can generate reports
- [ ] Google Sheets sync works
- [ ] Google Apps Script menu appears
- [ ] Data validation works in Google Sheets

---

## 📚 Next Steps

1. **Customize the application:**
   - Update company logo
   - Modify color scheme in `style.css`
   - Add custom fields to employee model

2. **Deploy to production:**
   - Use proper web server (Gunicorn)
   - Set up PostgreSQL database
   - Configure HTTPS
   - Use environment variables for secrets

3. **Enhance features:**
   - Add user authentication
   - Email notifications
   - Advanced reporting
   - Mobile responsive improvements

---

## 💡 Tips

- **Backup regularly:** Google Sheets has version history
- **Test in development:** Always test changes with sample data first
- **Monitor logs:** Check terminal output for errors
- **Keep credentials safe:** Never commit `credentials.json` to Git

---

## 📞 Getting Help

If you encounter issues:

1. **Check logs:** Terminal output shows detailed errors
2. **Read error messages:** They usually indicate the problem
3. **Verify configuration:** Double-check all setup steps
4. **Test components:** Isolate the issue (Flask, Sheets, Script)

---

**Good luck! 🚀**

You now have a complete employee tracking system with:
- ✅ Modern web dashboard
- ✅ Google Sheets integration
- ✅ Automated workflows
- ✅ Comprehensive reporting

Enjoy managing your team efficiently! 📊👥
