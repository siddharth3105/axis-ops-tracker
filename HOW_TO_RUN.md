# 🚀 How to Run Axis Ops Tracker - All Methods

Choose the method that works best for you!

---

## ⚡ Quick Methods (Easiest)

### Method 1: Use Batch File (Recommended for beginners)

**Steps:**
1. Double-click `start.bat`
2. Wait for setup to complete
3. Browser opens automatically

**Requirements:**
- Windows
- Python installed

---

### Method 2: Use PowerShell Script

**Steps:**
1. Right-click `quick_start.ps1`
2. Select "Run with PowerShell"
3. If error, run PowerShell as Admin first:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. Then run the script

**Requirements:**
- Windows
- Python installed
- PowerShell execution enabled

---

## 🔧 Manual Methods

### Method 3: Command Line (Step by Step)

**First Time Setup:**

```bash
# 1. Navigate to project folder
cd "C:\Users\SPURGE\AXIS AI TRACKER"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create sample data (optional)
python scripts\import_sample_data.py

# 6. Run the application
python run.py
```

**Subsequent Runs:**

```bash
# 1. Navigate to project
cd "C:\Users\SPURGE\AXIS AI TRACKER"

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Run the application
python run.py
```

---

### Method 4: Python Directly (No Virtual Environment)

⚠️ **Not recommended** - May cause package conflicts

```bash
# 1. Navigate to project
cd "C:\Users\SPURGE\AXIS AI TRACKER"

# 2. Install dependencies globally
pip install -r requirements.txt

# 3. Run the application
python run.py
```

---

## 🐍 If Python Commands Don't Work

Try these alternatives:

```bash
# Instead of: python
# Try:
py
python3
py -3
py -3.11

# Examples:
py -m venv venv
py run.py
py -3 scripts\import_sample_data.py
```

---

## 🌐 Accessing the Dashboard

Once the server starts, you'll see:

```
🚀 AXIS OPS TRACKER - Starting Server
📊 Dashboard will be available at: http://localhost:5000
```

**Open in browser:**
- http://localhost:5000
- http://127.0.0.1:5000

**Default pages:**
- Dashboard: http://localhost:5000/
- Employees: http://localhost:5000/employees/
- Analytics: http://localhost:5000/analytics/
- Payments: http://localhost:5000/payments/
- Reports: http://localhost:5000/reports/

---

## 🛑 Stopping the Server

**Press:** `CTRL + C` in the terminal

**Then:**
- Terminal returns to normal
- Can run again anytime

---

## 🔄 Restarting the Server

**After code changes:**
- Flask auto-reloads in debug mode
- Just save the file

**After dependency changes:**
```bash
pip install -r requirements.txt
```

**After model changes:**
```bash
# Delete database
del data\axis_ops.db

# Recreate
python scripts\import_sample_data.py

# Restart server
python run.py
```

---

## 📋 Complete First-Time Checklist

- [ ] Python 3.8+ installed
- [ ] Project folder extracted/cloned
- [ ] Opened terminal in project folder
- [ ] Created virtual environment
- [ ] Activated virtual environment
- [ ] Installed dependencies
- [ ] Created database
- [ ] Started server
- [ ] Opened browser to localhost:5000

---

## 🎯 Quick Reference Commands

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Install packages
pip install -r requirements.txt

# Import sample data
python scripts\import_sample_data.py

# Sync with Google Sheets
python scripts\google_sheets_integration.py

# Run application
python run.py

# Deactivate virtual environment
deactivate
```

---

## 🔍 Troubleshooting Quick Fixes

### "python is not recognized"
→ See: `INSTALL_PYTHON.md`

### "cannot be loaded because running scripts is disabled"
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Port 5000 already in use"
```bash
# Find process
netstat -ano | findstr :5000

# Kill it
taskkill /PID <number> /F
```

### "ModuleNotFoundError"
```bash
# Activate virtual environment!
.\venv\Scripts\activate

# Then install
pip install -r requirements.txt
```

### "No module named 'app'"
```bash
# Make sure you're in project root
cd "C:\Users\SPURGE\AXIS AI TRACKER"

# Check current directory
pwd
```

---

## 💡 Tips for Success

1. **Always activate virtual environment** before running
2. **Use the same terminal** for all commands
3. **Check you're in project folder** (`pwd` to verify)
4. **Read error messages** - they usually tell you what's wrong
5. **Restart terminal** if PATH changes don't work

---

## 🚀 Production Deployment

For production use (not localhost):

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or with specific settings
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 run:app
```

---

## 📊 Running with Sample Data vs Real Data

### With Sample Data (for testing):
```bash
python scripts\import_sample_data.py
python run.py
```
- Creates 30 sample employees
- Includes performance, payments, attendance
- Good for testing features

### With Real Data (from Google Sheets):
```bash
# Setup credentials first (see SETUP_GUIDE.md)
python scripts\google_sheets_integration.py
python run.py
```
- Imports from your actual spreadsheet
- Live sync with Google Sheets
- Real employee data

### With Both:
```bash
# Import samples first
python scripts\import_sample_data.py

# Then add real data
python scripts\google_sheets_integration.py

# Run
python run.py
```

---

## 🔐 Security Notes

**Development (localhost):**
- Safe to use default settings
- Only accessible from your computer

**Production (live server):**
- Change SECRET_KEY in app/__init__.py
- Use proper web server (gunicorn, nginx)
- Enable HTTPS
- Use strong database (PostgreSQL)
- Restrict access with authentication

---

## 📱 Accessing from Other Devices

**Same network only:**

1. Find your IP address:
   ```bash
   ipconfig
   # Look for IPv4 Address: 192.168.x.x
   ```

2. Run server on all interfaces:
   ```bash
   # Already set in run.py
   app.run(host='0.0.0.0', port=5000)
   ```

3. Access from other device:
   ```
   http://192.168.x.x:5000
   ```

**⚠️ Warning:** Only do this on trusted networks!

---

## 🎓 Learning the System

After getting it running:

1. **Explore the Dashboard**
   - View statistics
   - Check charts
   - See recent activity

2. **Add Test Employee**
   - Go to Employees page
   - Click "+ Add Employee"
   - Fill form and save

3. **View Analytics**
   - Performance metrics
   - Attendance tracking
   - Supervisor performance

4. **Generate Reports**
   - Go to Reports page
   - Generate various CSVs
   - Open in Excel

5. **Try Google Sheets Sync**
   - Setup credentials
   - Run sync script
   - See data appear

---

## 📞 Getting Help

If stuck, check in order:

1. **TROUBLESHOOTING.md** - Common issues
2. **SETUP_GUIDE.md** - Detailed setup steps
3. **INSTALL_PYTHON.md** - Python installation
4. **Error messages** - Read carefully
5. **Browser console** - Press F12

---

## ✅ Success Indicators

You know it's working when:

- ✅ Terminal shows "Running on http://..."
- ✅ No red error messages
- ✅ Browser opens to dashboard
- ✅ Charts display
- ✅ Numbers show in stat cards
- ✅ Can navigate between pages

---

## 🎉 You're Ready!

Choose your method and get started:

- **Easiest:** Double-click `start.bat`
- **Recommended:** Run `quick_start.ps1`
- **Manual:** Follow "Method 3" above
- **Troubleshooting:** See `TROUBLESHOOTING.md`

**The dashboard is waiting! 📊**
