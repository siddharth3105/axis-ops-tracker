# Google Sheets Integration - Setup Guide

## 📋 Overview

Your Axis Ops Tracker is configured to sync with this Google Sheet:
```
https://docs.google.com/spreadsheets/d/1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw/edit?usp=sharing
```

This guide will help you set up the Google Sheets API credentials.

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select existing project
3. Name it: **Axis Ops Tracker**
4. Click "Create"

### Step 2: Enable Google Sheets API

1. In your project, go to **APIs & Services** → **Enable APIs and Services**
2. Search for **Google Sheets API**
3. Click on it and click **Enable**
4. Also enable **Google Drive API** (search and enable)

### Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in details:
   - **Service account name**: `axis-ops-sync`
   - **Service account ID**: `axis-ops-sync@your-project.iam.gserviceaccount.com`
   - **Description**: Service account for Axis Ops Tracker Google Sheets sync
4. Click **Create and Continue**
5. Skip optional steps, click **Done**

### Step 4: Create Service Account Key

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Choose **JSON** format
5. Click **Create**
6. A JSON file will download automatically

### Step 5: Install the Credentials File

1. Rename the downloaded file to `credentials.json`
2. Move it to your project's `config` folder:
   ```
   C:\Users\SPURGE\AXIS AI TRACKER\config\credentials.json
   ```

### Step 6: Share Google Sheet with Service Account

1. Open the downloaded `credentials.json` file
2. Find the `client_email` field (looks like: `axis-ops-sync@your-project.iam.gserviceaccount.com`)
3. Copy that email address
4. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw/edit
5. Click **Share** button (top right)
6. Paste the service account email
7. Set permission to **Editor**
8. **Uncheck** "Notify people" (it's a service account, not a person)
9. Click **Share**

---

## ✅ Verify Setup

Run this test command:

```powershell
.\venv\Scripts\python.exe -c "from app.utils.google_sheets import GoogleSheetsSync; sync = GoogleSheetsSync(); print('✅ Connected!' if sync.connect() else '❌ Failed')"
```

If you see "✅ Connected!" - you're all set!

---

## 🔄 How to Sync Data

### Via Web Interface (Easiest)

1. Open http://localhost:5000
2. Click the **"Sync with Sheets"** button in the header
3. Wait for confirmation message
4. Open your Google Sheet to see the synced data

### Via API

```bash
curl -X POST http://localhost:5000/api/sync/sheets
```

### Programmatically

```python
from app.utils.google_sheets import GoogleSheetsSync

sync = GoogleSheetsSync()

# Sync specific data
sync.sync_employees(employees)
sync.sync_attendance(attendance_records)
sync.sync_qc_feedback(qc_records)
sync.sync_performance(performance_data)
sync.sync_payments(payments)

# Or sync everything
result = sync.sync_all()
print(result)
```

---

## 📊 What Gets Synced

The sync creates/updates these worksheets in your Google Sheet:

### 1. **Employees** Sheet
- Employee ID, Name, Email, Mobile
- Shift, Weekoff Day, Supervisor
- Status, Work Site
- Accommodation details
- Training dates

### 2. **Attendance** Sheet
- Date, Employee, Check-in/out times
- Hours worked, Work site
- GPS coordinates
- Validation status

### 3. **QC Feedback** Sheet
- Video ID, Task name, Duration
- QC Status, Approval percentage
- All 15 quality issue flags
- Reviewer comments

### 4. **Performance** Sheet
- Total days worked
- Production hours
- Quality percentage
- Total videos

### 5. **Payments** Sheet
- Payment date, Amount
- Hours processed
- Payment status
- Last payment date

---

## 🔄 Auto-Sync (Optional)

### Schedule Automatic Syncs

Create a scheduled task to sync every hour:

**Windows Task Scheduler:**

```powershell
# Create sync script
@'
cd "C:\Users\SPURGE\AXIS AI TRACKER"
.\venv\Scripts\python.exe -c "from app.utils.google_sheets import GoogleSheetsSync; from app import create_app; app = create_app(); app.app_context().push(); sync = GoogleSheetsSync(); result = sync.sync_all(); print(result)"
'@ | Out-File -FilePath "sync_sheets.ps1"

# Run hourly via Task Scheduler or cron
```

**Or use Python scheduler:**

```python
# In your app
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=sync_to_sheets,
    trigger="interval",
    hours=1
)
scheduler.start()
```

---

## 🛠️ Troubleshooting

### Error: "credentials.json not found"

**Solution:**
- Check the file is in `C:\Users\SPURGE\AXIS AI TRACKER\config\credentials.json`
- Make sure it's named exactly `credentials.json` (not `credentials.json.txt`)

### Error: "Permission denied" or "403"

**Solution:**
- Make sure you shared the Google Sheet with the service account email
- Check the email in `credentials.json` → `client_email` field
- Share permission must be "Editor", not "Viewer"

### Error: "Spreadsheet not found"

**Solution:**
- Verify the spreadsheet URL in `app/utils/google_sheets.py`
- Check the spreadsheet is not deleted or moved
- Ensure it's shared with the service account

### Error: "API not enabled"

**Solution:**
- Go to Google Cloud Console
- Enable both **Google Sheets API** and **Google Drive API**
- Wait a few minutes for changes to propagate

### Error: "Quota exceeded"

**Solution:**
- Google Sheets API has rate limits
- Reduce sync frequency
- Consider batch operations
- Check [Google API quotas](https://console.cloud.google.com/apis/api/sheets.googleapis.com/quotas)

---

## 🔒 Security Best Practices

### 1. Protect credentials.json

```powershell
# Add to .gitignore (already done)
echo "config/credentials.json" >> .gitignore
```

### 2. Rotate Keys Periodically

- Create new service account key every 90 days
- Delete old keys from Google Cloud Console
- Update credentials.json in your project

### 3. Limit Service Account Permissions

- Only grant "Editor" access to specific spreadsheet
- Don't make service account a domain-wide admin
- Use separate service accounts for production/development

### 4. Monitor API Usage

- Check Google Cloud Console → APIs & Services → Dashboard
- Set up alerts for unusual activity
- Review access logs periodically

---

## 📈 Advanced Usage

### Sync Specific Date Range

```python
from datetime import datetime, timedelta
from app.models import AttendanceRecord, Employee
from app import db

# Get last 7 days of attendance
start_date = datetime.now() - timedelta(days=7)
attendance = db.session.query(
    AttendanceRecord,
    Employee.name,
    Employee.employee_id
).join(Employee).filter(
    AttendanceRecord.attendance_date >= start_date.date()
).all()

# Sync
sync = GoogleSheetsSync()
sync.sync_attendance(attendance)
```

### Two-Way Sync (Import from Sheets)

```python
# Read from Google Sheet
worksheet = sync.spreadsheet.worksheet('Employees')
data = worksheet.get_all_records()

# Update database
for row in data:
    employee = Employee.query.filter_by(
        employee_id=row['Employee ID']
    ).first()
    if employee:
        employee.status = row['Status']
        employee.shift = row['Shift']
        # ... update other fields

db.session.commit()
```

### Custom Formatting

```python
# Add conditional formatting
worksheet.format('H2:H1000', {
    'backgroundColor': {
        'red': 0.9 if value == 'Rejected' else 0.3,
        'green': 0.3 if value == 'Rejected' else 0.9,
        'blue': 0.3
    }
})

# Add data validation
worksheet.add_validation(
    'G2:G1000',
    {
        'type': 'ONE_OF_LIST',
        'values': ['Active', 'Inactive']
    }
)
```

---

## 📞 Support

### Useful Links

- **Google Sheets API Documentation**: https://developers.google.com/sheets/api
- **gspread Library Docs**: https://docs.gspread.org/
- **Google Cloud Console**: https://console.cloud.google.com/
- **API Quotas**: https://console.cloud.google.com/apis/api/sheets.googleapis.com/quotas

### Common Issues

1. **Rate Limiting**: Wait and retry, or reduce sync frequency
2. **Permission Errors**: Re-share sheet with service account
3. **Connection Timeout**: Check internet connection
4. **Invalid Credentials**: Re-download service account key

---

## ✅ Post-Setup Checklist

- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service account created
- [ ] Service account key downloaded
- [ ] credentials.json in config folder
- [ ] Google Sheet shared with service account email
- [ ] Test connection successful
- [ ] First sync completed
- [ ] All 5 worksheets created in Google Sheet
- [ ] Data visible in Google Sheet

---

## 🎉 You're All Set!

Once setup is complete:

1. Click **"Sync with Sheets"** button in the app
2. Check your Google Sheet for the data
3. Schedule automatic syncs (optional)
4. Share the sheet with your team

Your Google Sheet will now serve as a live backup and reporting dashboard for your Axis Ops Tracker data!

---

**Spreadsheet URL**: https://docs.google.com/spreadsheets/d/1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw/edit?usp=sharing

**Last Updated**: Now
**Version**: 1.0.0
