# 📊 Axis Ops Tracker

A comprehensive employee tracking and management system built with **Python Flask** and **Google Sheets** integration. Track employees, monitor performance, manage payments, and generate reports—all in one powerful dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 📈 Dashboard
- Real-time statistics and KPIs
- Interactive charts and visualizations
- Recent activity tracking
- Shift and supervisor distribution analysis

### 👥 Employee Management
- Complete CRUD operations for employees
- Advanced search and filtering
- Bulk import from Google Sheets
- Employee profiles with detailed information

### 📊 Performance Analytics
- Top performers tracking (quality & production)
- Supervisor-wise performance analysis
- Attendance tracking and trends
- Quality metrics visualization

### 💰 Payment Management
- Payment tracking and history
- Status management (Pending/Processing/Completed)
- Payment summaries and reports
- Hours processed tracking

### 📄 Reports & Export
- Employee roster reports
- Performance reports
- Payment reports with date filtering
- Supervisor-wise team reports
- Export to CSV format

### 🔄 Google Sheets Integration
- Two-way sync with Google Sheets
- Automated data validation
- Real-time metrics calculation
- Automated backups

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google account (for Sheets integration)

### Installation

1. **Clone or download this project**
   ```bash
   cd "AXIS AI TRACKER"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   Navigate to: `http://localhost:5000`

---

## 📁 Project Structure

```
AXIS AI TRACKER/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── employee.py          # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Dashboard routes
│   │   ├── employees.py         # Employee management
│   │   ├── analytics.py         # Analytics & performance
│   │   ├── payments.py          # Payment tracking
│   │   └── reports.py           # Report generation
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Application styles
│   │   └── js/
│   │       └── main.js          # JavaScript functionality
│   └── templates/
│       ├── base.html            # Base template
│       ├── dashboard.html       # Dashboard page
│       ├── employees.html       # Employee management
│       ├── analytics.html       # Analytics page
│       ├── payments.html        # Payments page
│       └── reports.html         # Reports page
├── scripts/
│   ├── google_sheets_integration.py  # Python sync script
│   └── GoogleAppsScript.gs           # Google Apps Script
├── config/
│   └── credentials.json         # Google API credentials (create this)
├── data/
│   └── axis_ops.db              # SQLite database (auto-created)
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🔧 Configuration

### Google Sheets Integration Setup

#### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API and Google Drive API
4. Create service account credentials
5. Download credentials as `credentials.json`
6. Place in `config/` folder

#### 2. Share Google Sheet

1. Open your Google Sheet
2. Click "Share"
3. Add the service account email (from credentials.json)
4. Give "Editor" permissions

#### 3. Update Spreadsheet ID

Edit `scripts/google_sheets_integration.py`:
```python
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'
```

The spreadsheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
```

#### 4. Run Sync

```bash
python scripts/google_sheets_integration.py
```

### Google Apps Script Setup

1. Open your Google Sheet
2. Go to **Extensions > Apps Script**
3. Delete existing code
4. Copy content from `scripts/GoogleAppsScript.gs`
5. Save and authorize
6. Use the custom menu: **🔄 Axis Ops Tracker**

---

## 🎯 Usage Guide

### Adding Employees

1. Navigate to **Employees** page
2. Click **+ Add Employee**
3. Fill in the form
4. Click **Save Employee**

### Importing from Google Sheets

**Method 1: Python Script**
```bash
python scripts/google_sheets_integration.py
```

**Method 2: Dashboard**
1. Click **Sync with Sheets** button in header
2. Wait for confirmation

**Method 3: Google Apps Script**
1. In Google Sheets, go to **🔄 Axis Ops Tracker > Sync to Dashboard**

### Generating Reports

1. Go to **Reports** page
2. Select report type
3. Choose date range (for payment reports)
4. Click **Generate**
5. CSV file will download automatically

### Analytics

- View performance metrics in **Analytics** page
- Charts show:
  - Top performers by quality
  - Top performers by production hours
  - Supervisor performance comparison
  - Daily attendance trends

---

## 📊 Database Schema

### Employees Table
- Personal information (ID, name, email, mobile)
- Work details (shift, supervisor, work site)
- Status and accommodation info
- Dates (joining, training)

### Performance Table
- Total days worked
- Total production hours
- Quality percentage
- Total videos processed

### Payments Table
- Payment dates
- Hours processed
- Amount transferred
- Payment status

### Attendance Table
- Daily attendance records
- Hours worked per day
- Status (Present/Absent/Leave)

---

## 🔒 Security Notes

- Store `credentials.json` securely
- Don't commit `credentials.json` to version control
- Change the `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS in production

---

## 🛠️ Development

### Running in Development Mode

```bash
python run.py
```

The server will start at `http://localhost:5000` with auto-reload enabled.

### Running in Production

**Using Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Environment Variables:**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
```

---

## 📝 API Endpoints

### Dashboard
- `GET /` - Dashboard page
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/recent-activity` - Recent activity

### Employees
- `GET /employees/api/list` - List all employees
- `GET /employees/api/<id>` - Get employee details
- `POST /employees/api/create` - Create employee
- `PUT /employees/api/<id>/update` - Update employee
- `DELETE /employees/api/<id>/delete` - Delete employee

### Analytics
- `GET /analytics/api/performance/overview` - Performance metrics
- `GET /analytics/api/attendance/summary` - Attendance data

### Payments
- `GET /payments/api/list` - List payments
- `POST /payments/api/create` - Create payment
- `PUT /payments/api/<id>/update` - Update payment

### Reports
- `GET /reports/api/generate/employee-roster` - Employee roster CSV
- `GET /reports/api/generate/performance-report` - Performance CSV
- `GET /reports/api/generate/payment-report` - Payment CSV
- `GET /reports/api/generate/supervisor-report` - Supervisor CSV

---

## 🐛 Troubleshooting

### Database Issues

**Reset database:**
```bash
# Delete existing database
rm data/axis_ops.db

# Restart application (will recreate)
python run.py
```

### Google Sheets Sync Errors

1. Check `credentials.json` is in `config/` folder
2. Verify service account has access to sheet
3. Check spreadsheet ID is correct
4. Ensure APIs are enabled in Google Cloud Console

### Module Not Found Errors

```bash
pip install -r requirements.txt --upgrade
```

---

## 📚 Technologies Used

- **Backend:** Flask 3.0, SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript ES6
- **Charts:** Chart.js
- **Database:** SQLite (development), PostgreSQL (recommended for production)
- **Integration:** Google Sheets API, Google Apps Script
- **Icons:** Font Awesome 6

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the setup instructions
3. Check application logs in the terminal

---

## 🎉 Features Roadmap

- [ ] User authentication and role-based access
- [ ] Email notifications for payment updates
- [ ] Mobile app (React Native)
- [ ] Advanced reporting with PDF export
- [ ] Bulk employee operations
- [ ] Integration with payroll systems
- [ ] Real-time dashboard updates
- [ ] Dark mode theme

---

**Built with ❤️ for Axis Operations Team**

---

## 📸 Screenshots

### Dashboard
Beautiful dashboard with real-time statistics, charts, and recent activity.

### Employee Management
Complete employee management with search, filters, and easy editing.

### Analytics
Powerful analytics with performance tracking and attendance monitoring.

### Payment Tracking
Track all payments with status management and comprehensive history.

### Reports
Generate detailed reports and export to CSV for further analysis.

---

**Version:** 1.0.0  
**Last Updated:** October 2026
