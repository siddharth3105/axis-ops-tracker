# 🐍 Python Installation Guide for Windows

If you don't have Python installed, follow this guide step-by-step.

---

## ⚡ Quick Install (Recommended)

### Step 1: Download Python

1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow button: **"Download Python 3.11.x"** (or latest version)
3. Wait for download to complete

### Step 2: Install Python

1. **Double-click** the downloaded file (e.g., `python-3.11.x-amd64.exe`)
2. **⚠️ IMPORTANT:** Check the box that says **"Add Python to PATH"**
3. Click **"Install Now"**
4. Wait for installation to complete (2-3 minutes)
5. Click **"Close"** when finished

### Step 3: Verify Installation

1. Open **PowerShell** or **Command Prompt**
   - Press `Windows + R`
   - Type `powershell`
   - Press Enter

2. Type this command and press Enter:
   ```bash
   python --version
   ```

3. You should see something like:
   ```
   Python 3.11.x
   ```

✅ **Success!** Python is installed. Now you can run the tracker:
```bash
cd "C:\Users\SPURGE\AXIS AI TRACKER"
.\start.bat
```

---

## 🔧 Detailed Installation Steps (with Screenshots)

### 1. Download Python

#### Option A: From Python.org (Recommended)
- Visit: https://www.python.org/downloads/
- Click "Download Python 3.x.x"
- Save to Downloads folder

#### Option B: Direct Links
- **Python 3.11:** https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
- **Python 3.10:** https://www.python.org/ftp/python/3.10.13/python-3.10.13-amd64.exe

### 2. Run the Installer

**⚠️ CRITICAL STEP:**
```
┌─────────────────────────────────────────┐
│ Install Python 3.11                      │
│                                          │
│ ☑ Add Python to PATH  ← CHECK THIS BOX! │
│                                          │
│ [ Install Now ]                          │
│ [ Customize Installation ]               │
│                                          │
└─────────────────────────────────────────┘
```

**Why is this important?**
- Without this, Windows won't find Python
- You'll get "python is not recognized" errors
- You'll need to add it manually later

### 3. Installation Options

Choose one:

#### A. Quick Install (Easier)
1. Check "Add Python to PATH"
2. Click "Install Now"
3. Done!

#### B. Custom Install (Advanced)
1. Check "Add Python to PATH"
2. Click "Customize Installation"
3. Keep all default options checked
4. Click "Next"
5. Check "Install for all users" (optional)
6. Click "Install"

### 4. Wait for Installation

You'll see:
```
Installing Python 3.11...
[████████████████████] 100%
Setup was successful
```

### 5. Verify Installation

Open PowerShell and test:

```powershell
# Test Python
python --version

# Test pip (package manager)
pip --version

# Both should show version numbers
```

---

## 🔄 Alternative: Microsoft Store

### Easy Installation

1. Open **Microsoft Store** app
2. Search for **"Python 3.11"**
3. Click **"Get"** or **"Install"**
4. Wait for installation
5. Done! (PATH is set automatically)

**Pros:**
- Automatic updates
- No manual PATH setup
- Easy uninstall

**Cons:**
- May have permission issues
- Slightly older versions

---

## 🚨 Troubleshooting Python Installation

### Issue: "Add to PATH" was forgotten

**Fix manually:**

1. Find Python installation folder:
   - Usually: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`

2. Open Environment Variables:
   - Press `Windows + R`
   - Type: `sysdm.cpl`
   - Click "Environment Variables"

3. Edit PATH:
   - Under "User variables", select "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311`
   - Click "New" again
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts`
   - Click OK on all windows

4. **Restart PowerShell/CMD**

5. Test: `python --version`

### Issue: Multiple Python versions

**Use specific version:**
```bash
# Python 3
py -3 --version

# Python 3.11 specifically
py -3.11 --version

# Use in project
py -3.11 -m venv venv
```

### Issue: Python opens Microsoft Store

**Fix:**

1. Press `Windows + I` (Settings)
2. Go to "Apps"
3. Click "Apps & Features"
4. Click "App execution aliases"
5. Turn OFF the Python aliases

### Issue: "Python was not found"

**Reasons:**
1. Not installed
2. Not in PATH
3. PowerShell not restarted after install

**Solutions:**
1. Reinstall Python (check the PATH box!)
2. Add to PATH manually (see above)
3. Close and reopen PowerShell/CMD
4. Try `py` or `python3` instead of `python`

---

## ✅ Verification Checklist

Test these commands (all should work):

```bash
# Basic Python
python --version

# Alternative command
py --version

# Package manager
pip --version

# Virtual environment
python -m venv test_env

# Delete test
rmdir /s /q test_env
```

If all work, you're ready! ✅

---

## 🎯 Next Steps

Now that Python is installed:

### Option 1: Quick Start
```bash
cd "C:\Users\SPURGE\AXIS AI TRACKER"
.\start.bat
```

### Option 2: Manual Steps
```bash
cd "C:\Users\SPURGE\AXIS AI TRACKER"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python scripts\import_sample_data.py
python run.py
```

---

## 📦 What Gets Installed

When you install Python, you get:

- **Python interpreter** - Runs Python code
- **pip** - Package installer
- **IDLE** - Basic Python editor
- **Standard library** - Built-in modules
- **Documentation** - Help files

Size: ~100 MB

---

## 🔄 Updating Python

### Check current version:
```bash
python --version
```

### To update:
1. Download newer version from python.org
2. Run installer
3. Choose "Upgrade Now"

### Using pip:
```bash
python -m pip install --upgrade pip
```

---

## 🗑️ Uninstalling Python

If you need to uninstall:

1. Press `Windows + I` (Settings)
2. Go to "Apps"
3. Search for "Python"
4. Click and select "Uninstall"

Or:

1. Go to Control Panel
2. Programs and Features
3. Find Python
4. Uninstall

---

## 💡 Tips

- **Always check "Add to PATH"** during installation
- **Restart terminal** after installation
- **Use latest stable version** (3.11+ recommended)
- **Don't install to Program Files** (use default location)
- **Keep pip updated:** `python -m pip install --upgrade pip`

---

## 🎓 Learning Resources

After installation, learn Python:

- **Official Tutorial:** https://docs.python.org/3/tutorial/
- **Python for Beginners:** https://www.python.org/about/gettingstarted/
- **Interactive Tutorial:** https://www.learnpython.org/

---

## ⚙️ System Requirements

- **Windows:** 7 or later (64-bit recommended)
- **Disk Space:** 100 MB minimum
- **RAM:** 512 MB minimum
- **Internet:** For downloading packages

---

## 🆘 Still Need Help?

**Can't install Python?**

Try:
1. Anaconda (includes Python): https://www.anaconda.com/download
2. WinPython (portable): https://winpython.github.io/
3. Ask IT department for assistance

**Alternative:**
Use the online version (if available) or request pre-configured setup.

---

**Once Python is installed, return to the main README.md to continue setup!**
