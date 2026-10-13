# 📊 AXIS OPS TRACKER - START HERE

Welcome! This is your complete employee tracking system.

---

## ⚡ FASTEST WAY TO START

### Windows Users (Easiest):

**1. Double-click:** `start.bat`  
**2. Wait:** System sets up automatically  
**3. Open browser:** http://localhost:5000  

**That's it!** 🎉

---

## 📚 Documentation Guide

Based on your situation, start with the right guide:

### 🆕 First Time Users

1. **Don't have Python?**
   - Read: `INSTALL_PYTHON.md`
   - Install Python first

2. **Have Python, ready to start?**
   - Read: `HOW_TO_RUN.md`
   - Pick your preferred method

3. **Want complete understanding?**
   - Read: `README.md`
   - Full project documentation

### 🔧 Setup Guides

4. **Need detailed setup instructions?**
   - Read: `SETUP_GUIDE.md`
   - Step-by-step with Google Sheets integration

5. **Having problems?**
   - Read: `TROUBLESHOOTING.md`
   - Solutions to common issues

### 📖 Reference

6. **Project Overview**
   - Read: `README.md`
   - Features, architecture, API docs

---

## 🎯 Quick Decision Tree

```
Do you have Python installed?
│
├─ NO → Read INSTALL_PYTHON.md → Install Python
│        └─ Then come back here
│
└─ YES → Is this your first time running?
         │
         ├─ YES → Use start.bat (double-click)
         │        └─ Or read HOW_TO_RUN.md
         │
         └─ NO → Just run: python run.py
                  └─ Or use start.bat
```

---

## 🚀 Three Ways to Run

### Method 1: Batch File (Easiest)
```
Double-click: start.bat
```

### Method 2: PowerShell Script
```powershell
.\quick_start.ps1
```

### Method 3: Manual Commands
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python scripts\import_sample_data.py
python run.py
```

---

## 📋 What You Need

✅ **Required:**
- Windows PC
- Python 3.8 or higher
- Internet connection (for setup)
- Web browser

✅ **Optional (for Google Sheets sync):**
- Google account
- Google Cloud credentials
- Access to the Axis Ops spreadsheet

---

## 🎨 What You'll Get

### **Dashboard** 📊
- Real-time employee statistics
- Performance charts
- Recent activity feed
- Supervisor distribution

### **Employee Management** 👥
- Add/edit/delete employees
- Search and filter
- Complete employee profiles
- Import from Google Sheets

### **Analytics** 📈
- Top performers tracking
- Quality metrics
- Attendance monitoring
- Supervisor performance

### **Payment Tracking** 💰
- Payment history
- Status management
- Amount tracking
- Payment reports

### **Reports** 📄
- Employee roster
- Performance reports
- Payment reports
- Supervisor reports
- Export to CSV/Excel

---

## 🗂️ Project Structure

```
AXIS AI TRACKER/
│
├── 📄 START_HERE.md              ← You are here!
├── 📄 README.md                  ← Complete documentation
├── 📄 SETUP_GUIDE.md             ← Detailed setup steps
├── 📄 HOW_TO_RUN.md              ← All ways to run the app
├── 📄 TROUBLESHOOTING.md         ← Problem solutions
├── 📄 INSTALL_PYTHON.md          ← Python installation help
│
├── 🚀 start.bat                  ← Quick start (Windows)
├── 🚀 quick_start.ps1            ← PowerShell quick start
├── 🚀 run.py                     ← Main application file
├── 📋 requirements.txt           ← Python dependencies
│
├── 📁 app/                       ← Flask application
│   ├── models/                   ← Database models
│   ├── routes/                   ← API endpoints
│   ├── static/                   ← CSS & JavaScript
│   └── templates/                ← HTML pages
│
├── 📁 scripts/                   ← Utilities
│   ├── import_sample_data.py    ← Create test data
│   ├── google_sheets_integration.py ← Sync with Sheets
│   └── GoogleAppsScript.gs      ← Google Sheets automation
│
├── 📁 config/                    ← Configuration files
├── 📁 data/                      ← Database (auto-created)
└── 📁 venv/                      ← Virtual environment (auto-created)
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Install Python (if needed) | 5 minutes |
| First-time setup | 5 minutes |
| Reading documentation | 15 minutes |
| Google Sheets setup | 15 minutes |
| **Total first-time** | **30-40 minutes** |
| **Subsequent runs** | **30 seconds** |

---

## 🎓 Learning Path

### Day 1: Get it Running
1. Install Python (if needed)
2. Run `start.bat`
3. Explore the dashboard
4. Add a test employee

### Day 2: Understand the System
1. Read `README.md`
2. Try all features
3. Generate some reports
4. Check analytics

### Day 3: Real Data
1. Read `SETUP_GUIDE.md`
2. Set up Google Sheets integration
3. Import your real data
4. Customize as needed

---

## 💡 Pro Tips

1. **Start simple:** Use sample data first
2. **Test everything:** Try all features before real data
3. **Read errors:** They tell you what's wrong
4. **Keep terminal open:** See what's happening
5. **Backup data:** Before major changes

---

## 🆘 Quick Help

### I get "Python not found"
→ Read: `INSTALL_PYTHON.md`

### Scripts won't run
→ Read: `TROUBLESHOOTING.md` → PowerShell section

### Database errors
→ Delete `data/axis_ops.db` and run `scripts\import_sample_data.py`

### Google Sheets not working
→ Read: `SETUP_GUIDE.md` → Section 2

### Everything is broken
→ Read: `TROUBLESHOOTING.md` → Emergency Reset section

---

## 📊 Features Checklist

Try these after setup:

- [ ] View dashboard with charts
- [ ] Add a new employee
- [ ] Edit employee information
- [ ] Search and filter employees
- [ ] View analytics page
- [ ] Check top performers
- [ ] Add a payment record
- [ ] Generate an employee roster report
- [ ] Generate a performance report
- [ ] Export data to CSV

---

## 🎯 Common First-Time Questions

**Q: Do I need to install anything else?**  
A: Just Python. Everything else installs automatically.

**Q: Will it work on my computer?**  
A: Yes, if you have Windows and Python 3.8+.

**Q: Is my data safe?**  
A: Yes, everything is stored locally on your computer.

**Q: Can I use it without Google Sheets?**  
A: Yes! Google Sheets is optional. Use sample data or add manually.

**Q: How do I stop it?**  
A: Press CTRL+C in the terminal window.

**Q: Can others access it?**  
A: Not unless you specifically share it on your network.

---

## 🚦 Status Indicators

When running successfully, you'll see:

```
✓ Python found
✓ Virtual environment created
✓ Dependencies installed
✓ Database created
✓ Server running on http://localhost:5000
```

If you see red ✗ marks, check `TROUBLESHOOTING.md`.

---

## 🎉 Ready to Start?

### Choose Your Path:

**🏃 Quick Start (Recommended):**
```
1. Double-click: start.bat
2. Open browser: http://localhost:5000
3. Start tracking!
```

**📖 Learn First:**
```
1. Read: README.md
2. Read: HOW_TO_RUN.md
3. Follow steps
```

**🛠️ Custom Setup:**
```
1. Read: SETUP_GUIDE.md
2. Configure Google Sheets
3. Import real data
```

---

## 📞 Need More Help?

1. **Check the docs** in this folder
2. **Read error messages** carefully
3. **Try troubleshooting guide** first
4. **Search for specific errors** in TROUBLESHOOTING.md

---

## 🎊 What's Next?

After getting it running:

- **Customize:** Change colors, add features
- **Import real data:** Use your actual employee spreadsheet
- **Deploy:** Set up on a server for team access
- **Extend:** Add new features as needed

---

**Everything is ready! Pick a method and get started! 🚀**

---

### Quick Links:

- 📘 [Complete Guide](README.md)
- 🏃 [How to Run](HOW_TO_RUN.md)
- 🔧 [Setup Instructions](SETUP_GUIDE.md)
- 🐍 [Install Python](INSTALL_PYTHON.md)
- 🆘 [Troubleshooting](TROUBLESHOOTING.md)

---

**Made with ❤️ for Axis Operations Team**

**Version 1.0 | October 2026**
