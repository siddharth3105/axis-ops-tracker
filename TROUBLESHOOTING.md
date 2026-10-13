# 🔧 Troubleshooting Guide - Axis Ops Tracker

This guide covers common issues and their solutions.

---

## 🐍 Python Issues

### Issue: "Python not found" or "python is not recognized"

**Cause:** Python is not installed or not in system PATH.

**Solutions:**

1. **Install Python:**
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT:** Check "Add Python to PATH" during installation
   - Restart your terminal/PowerShell after installation

2. **Verify Installation:**
   ```bash
   python --version
   # or
   py --version
   # or
   python3 --version
   ```

3. **Manual PATH Setup (if forgot to check the box):**
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X`
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts`
   - Restart terminal

### Issue: "python -m venv venv" fails

**Solutions:**

1. **Try alternative commands:**
   ```bash
   py -m venv venv
   # or
   python3 -m venv venv
   ```

2. **Install/upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Use different Python version:**
   ```bash
   py -3.10 -m venv venv
   ```

---

## 📦 Virtual Environment Issues

### Issue: Cannot activate virtual environment

**Cause:** PowerShell execution policy restrictions.

**Solutions:**

1. **Allow script execution (Run PowerShell as Administrator):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Use the batch file instead:**
   ```bash
   start.bat
   ```

3. **Activate manually:**
   ```bash
   .\venv\Scripts\activate
   ```

### Issue: "venv\Scripts\activate.ps1 cannot be loaded"

**Solution:**
```powershell
# Run in PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
```

Then try again.

---

## 📚 Dependency Installation Issues

### Issue: pip install fails with permission error

**Solutions:**

1. **Run as Administrator:**
   - Right-click PowerShell/CMD
   - Choose "Run as Administrator"

2. **Use --user flag:**
   ```bash
   pip install -r requirements.txt --user
   ```

3. **Upgrade pip first:**
   ```bash
   python -m pip install --upgrade pip
   ```

### Issue: "Microsoft Visual C++ 14.0 is required"

**Solution:**
Download and install: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Or use pre-built wheels:
```bash
pip install --only-binary :all: -r requirements.txt
```

### Issue: Specific package fails (e.g., google-auth)

**Solution:**
```bash
# Install problematic packages separately
pip install google-auth --no-cache-dir
pip install gspread --no-cache-dir
pip install -r requirements.txt
```

---

## 🗄️ Database Issues

### Issue: Database file not found

**Solution:**
The database is created automatically. Just run:
```bash
python scripts\import_sample_data.py
```

### Issue: Database locked or corrupted

**Solutions:**

1. **Delete and recreate:**
   ```bash
   # Delete database
   del data\axis_ops.db
   
   # Recreate with sample data
   python scripts\import_sample_data.py
   ```

2. **Close all connections:**
   - Stop the Flask server (CTRL+C)
   - Close any database browsers
   - Restart the application

### Issue: "Table already exists" error

**Solution:**
```bash
# Delete database and start fresh
rmdir /s /q data
mkdir data
python scripts\import_sample_data.py
```

---

## 🌐 Flask Server Issues

### Issue: "Port 5000 is already in use"

**Solutions:**

1. **Find and kill the process:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   ```

2. **Use different port:**
   Edit `run.py`:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

3. **Common port conflicts:**
   - AirPlay Receiver (macOS) uses port 5000
   - Some VPN software uses port 5000

### Issue: Server starts but browser shows "Connection refused"

**Solutions:**

1. **Check if server is actually running:**
   - Look for "Running on http://..." message
   - Make sure no errors in terminal

2. **Try different URL:**
   ```
   http://localhost:5000
   http://127.0.0.1:5000
   http://0.0.0.0:5000
   ```

3. **Check firewall:**
   - Windows Defender may be blocking
   - Add Python to allowed apps

### Issue: "ModuleNotFoundError" when running Flask

**Cause:** Virtual environment not activated or packages not installed.

**Solution:**
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run again
python run.py
```

---

## 📊 Google Sheets Integration Issues

### Issue: "credentials.json not found"

**Solution:**
1. Follow SETUP_GUIDE.md to create Google Cloud credentials
2. Download the JSON file
3. Rename to `credentials.json`
4. Place in `config/` folder

### Issue: "gspread.exceptions.APIError: PERMISSION_DENIED"

**Causes & Solutions:**

1. **Service account not added to sheet:**
   - Open Google Sheet
   - Click "Share"
   - Add service account email from credentials.json
   - Give "Editor" permission

2. **APIs not enabled:**
   - Go to Google Cloud Console
   - Enable "Google Sheets API"
   - Enable "Google Drive API"

3. **Wrong spreadsheet ID:**
   - Check `scripts/google_sheets_integration.py`
   - Verify `SPREADSHEET_ID` matches your sheet

### Issue: "No module named 'gspread'"

**Solution:**
```bash
pip install gspread oauth2client google-auth
```

---

## 🎨 Frontend Issues

### Issue: Charts not displaying

**Causes & Solutions:**

1. **No data in database:**
   ```bash
   python scripts\import_sample_data.py
   ```

2. **JavaScript errors:**
   - Open browser console (F12)
   - Check for errors
   - Refresh page (CTRL+F5)

3. **CDN blocked:**
   - Check internet connection
   - Try different browser

### Issue: CSS not loading / page looks broken

**Solutions:**

1. **Clear browser cache:**
   - Press CTRL+SHIFT+DELETE
   - Clear cached files
   - Refresh page

2. **Check file paths:**
   - Verify `app/static/css/style.css` exists
   - Restart Flask server

3. **Hard refresh:**
   - Press CTRL+F5
   - Or CTRL+SHIFT+R

---

## 🔐 Security/Permission Issues

### Issue: "Access Denied" when creating files

**Solution:**
- Run terminal as Administrator
- Or move project to user folder (Documents, Desktop, etc.)

### Issue: Antivirus blocking execution

**Solution:**
- Add project folder to antivirus exclusions
- Temporarily disable antivirus during setup
- Whitelist Python and pip

---

## 💾 Data Import Issues

### Issue: Sample data script fails

**Solution:**
```bash
# Delete existing database
del data\axis_ops.db

# Run with verbose output
python scripts\import_sample_data.py
```

Check terminal output for specific error.

### Issue: Google Sheets sync fails

**Checklist:**
- [ ] credentials.json in config/ folder
- [ ] Service account has access to sheet
- [ ] Spreadsheet ID is correct
- [ ] APIs enabled in Google Cloud
- [ ] Internet connection working

**Debug:**
```python
# Test connection
python -c "import gspread; from oauth2client.service_account import ServiceAccountCredentials; print('✓ Imports work')"
```

---

## 🖥️ System-Specific Issues

### Windows

**PowerShell script won't run:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\quick_start.ps1
```

**Use batch file instead:**
```bash
start.bat
```

### macOS/Linux

**Script compatibility:**
Use bash instead:
```bash
# Create bash version
chmod +x setup.sh
./setup.sh
```

---

## 🔍 Debugging Steps

### General Debugging Process:

1. **Check Python:**
   ```bash
   python --version
   ```

2. **Check virtual environment:**
   ```bash
   .\venv\Scripts\activate
   pip list
   ```

3. **Check imports:**
   ```bash
   python -c "import flask; import sqlalchemy; print('✓ Imports OK')"
   ```

4. **Check database:**
   ```bash
   python -c "from app import create_app, db; app = create_app(); print('✓ Database OK')"
   ```

5. **Run with verbose errors:**
   ```bash
   python run.py
   # Look at full error traceback
   ```

---

## 📞 Getting More Help

### Check Logs

1. **Terminal output:** Read error messages carefully
2. **Browser console:** Press F12 → Console tab
3. **Python traceback:** Full error details

### Common Error Patterns

| Error Message | Solution |
|---------------|----------|
| "Module not found" | Install package: `pip install <package>` |
| "Permission denied" | Run as Administrator |
| "Port in use" | Change port or kill process |
| "File not found" | Check file paths and current directory |
| "Import error" | Activate virtual environment |

---

## ✅ Quick Fixes Checklist

Before asking for help, try these:

- [ ] Restart terminal/PowerShell
- [ ] Activate virtual environment: `.\venv\Scripts\activate`
- [ ] Update pip: `python -m pip install --upgrade pip`
- [ ] Reinstall packages: `pip install -r requirements.txt --force-reinstall`
- [ ] Delete and recreate database
- [ ] Clear browser cache
- [ ] Try different browser
- [ ] Run as Administrator
- [ ] Check antivirus/firewall
- [ ] Verify internet connection

---

## 🚑 Emergency Reset

If nothing works, complete reset:

```bash
# 1. Backup any custom data
# 2. Delete everything except source files
rmdir /s /q venv
rmdir /s /q data
rmdir /s /q __pycache__
del *.pyc

# 3. Fresh start
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python scripts\import_sample_data.py
python run.py
```

---

## 📚 Additional Resources

- **Python Documentation:** https://docs.python.org/3/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Google Sheets API:** https://developers.google.com/sheets/api
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/

---

**Still having issues?** 

1. Copy the full error message
2. Note what you were trying to do
3. Check if similar issue is listed above
4. Review SETUP_GUIDE.md for step-by-step instructions

Most issues are due to:
- Python not in PATH
- Virtual environment not activated
- Packages not installed
- Wrong Python version (need 3.8+)
