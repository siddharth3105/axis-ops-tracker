# Attendance & QC Features - Setup Guide

## 📋 Overview

This integration adds two major features to Axis Ops Tracker:

1. **QR-Based Attendance Tracking** - GPS-validated check-in/check-out system
2. **QC Video Feedback System** - Quality control for employee training videos

---

## 🚀 Quick Setup

### Step 1: Run Setup Script

```powershell
.\venv\Scripts\python.exe scripts\setup_attendance_qc.py
```

This will:
- ✅ Create new database tables (attendance_records, qc_feedback, work_sites)
- ✅ Add 4 sample work sites with QR codes
- ✅ Generate 30 days of attendance data
- ✅ Create 100 sample QC feedback records

### Step 2: Start the Server

```powershell
.\venv\Scripts\python.exe run.py
```

### Step 3: Access New Features

- **Attendance Tracking**: http://localhost:5000/attendance/
- **QC Feedback**: http://localhost:5000/qc/

---

## 📱 Attendance Tracking System

### Based on Work Attendance App User Guide (Provided Document)

**Key Features:**
- QR code-based check-in/check-out
- GPS location validation (150m radius, 100m accuracy)
- Support for residents (check-in only) and non-residents (check-in/check-out)
- Auto-checkout after 15 hours
- 5-minute grace period to prevent accidental checkout

**Work Sites:**
- Site A: Main Office
- Site B: Production Floor A  
- Site C: Production Floor B
- Site D: Warehouse

Each site has unique QR code and GPS coordinates for validation.

**API Endpoints:**
- `POST /attendance/api/check-in` - Process QR scan
- `GET /attendance/api/today-status/<employee_id>` - Check today's status
- `GET /attendance/api/list` - List attendance with filters
- `GET /attendance/api/summary` - Dashboard statistics

### How It Works:

1. **Employee scans QR code** at work site
2. **System validates**:
   - Employee is Active
   - QR code is registered
   - GPS accuracy < 100m
   - Location within 150m of work site
3. **Check-in recorded** with timestamp and GPS
4. **For non-residents**: Second scan = check-out (after 5 min grace)
5. **For residents**: One scan per day only

---

## 📹 QC Feedback System

### Based on QC Feedback Document (Provided Document)

**Quality Issues Tracked:**
- ✅ Wrist Camera Mismatch/Not Worn
- ✅ Hands Not Visible
- ✅ Poor Lighting
- ✅ Wrong Environment
- ✅ Shaky/Unstable Camera
- ✅ Video Too Short (< 1 min)
- ✅ Head Cap Not Worn
- ✅ Wrong Task Selected
- ✅ Video Not Playing/Missing Data
- ✅ Blurry/Glitching Video
- ✅ Task Too Slow/Dragging
- ✅ Irrelevant/Fake Video
- ✅ Pretending/Acting
- ✅ Rejected on Re-check

**QC Statuses:**
- **Pending** - Awaiting review
- **Approved** - Quality acceptable (typically 60%+ approval)
- **Rejected** - Quality issues found
- **Trimmed** - Edited version approved

**Collector Performance:**
Based on actual QC data from the document, tracking:
- Total videos recorded
- Approval rate
- Common rejection reasons
- Individual collector statistics

**API Endpoints:**
- `POST /qc/api/submit` - Submit QC feedback
- `GET /qc/api/list` - List feedback with filters
- `GET /qc/api/<id>` - Get specific feedback
- `PUT /qc/api/<id>/update` - Update feedback
- `GET /qc/api/summary` - Dashboard statistics
- `GET /qc/api/employee/<id>/stats` - Employee QC performance

---

## 📊 Dashboard Integration

Both features are integrated into the main navigation:

```
Dashboard → Employees → Attendance → QC Feedback → Analytics → Payments → Reports
```

**Dashboard Stats Added:**
- Today's check-ins/check-outs
- QC approval rates
- Top performers
- Common quality issues

---

## 🗄️ Database Models

### AttendanceRecord
- employee_id (FK)
- attendance_date
- check_in_time, check_out_time
- GPS coordinates (check-in & check-out)
- work_site_id
- qr_code_scanned
- hours_worked
- status (Checked In, Checked Out, Auto Checkout)
- is_valid, validation_message

### QCFeedback
- employee_id (FK)
- video_id, task_name
- video_duration, recorded_date
- qc_status (Pending, Approved, Rejected, Trimmed)
- approval_percentage
- 15 boolean fields for different quality issues
- qc_comments, qc_reviewer
- submitted_date, reviewed_date

### WorkSite
- site_id (unique)
- site_name
- latitude, longitude
- allowed_radius_meters (default: 150)
- gps_accuracy_limit_meters (default: 100)
- is_active
- qr_code_data (unique)

---

## 🔧 Configuration

### Attendance Settings

Edit in `app/models/attendance_qc.py` or create admin panel:

```python
# GPS Validation
allowed_radius_meters = 150  # Distance from work site
gps_accuracy_limit_meters = 100  # Required GPS precision

# Checkout Settings
AUTO_CHECKOUT_HOURS = 15  # Auto-checkout after X hours
CHECKOUT_GRACE_PERIOD_MINUTES = 5  # Prevent accidental checkout
```

### QC Settings

Quality thresholds can be configured:

```python
# Approval Thresholds
APPROVAL_THRESHOLD = 60  # % for approval
REJECTION_THRESHOLD = 50  # % for rejection
```

---

## 📱 Mobile App Integration

### QR Code Generation

For attendance QR codes:

```python
import qrcode

work_site = WorkSite.query.filter_by(site_id='SITE_A').first()
qr_data = work_site.qr_code_data

qr = qrcode.make(qr_data)
qr.save(f'qr_{work_site.site_id}.png')
```

### API Authentication

For mobile apps, add authentication:

```python
from flask_httpauth import HTTPBasicAuth
# or
from flask_jwt_extended import JWTManager
```

---

## 📈 Reports & Analytics

### Attendance Reports

```python
# Daily attendance report
GET /attendance/api/list?attendance_date=2026-01-15

# Employee attendance history
GET /attendance/api/list?employee_id=5&start_date=2026-01-01

# Work site utilization
GET /attendance/api/list?work_site_id=SITE_A
```

### QC Reports

```python
# Collector performance
GET /qc/api/employee/5/stats

# Issue breakdown
GET /qc/api/summary

# Filter by status
GET /qc/api/list?status=Rejected&start_date=2026-01-01
```

---

## 🐛 Troubleshooting

### Attendance Issues

**"GPS accuracy too low"**
- User needs to move outdoors or near window
- GPS accuracy must be < 100m

**"Outside allowed attendance location"**
- User is > 150m from work site
- Check work site coordinates are correct
- Verify QR code matches correct work site

**"Attendance already recorded"**
- For residents: One check-in per day only
- For non-residents: Can't check-out within 5 minutes of check-in

### QC Issues

**Videos not loading**
- Check `video_id` format
- Verify file paths in database

**Approval percentage calculation**
- Approval % = (approved videos / total videos) × 100
- Calculated automatically based on QC status

---

## 🔒 Security Considerations

1. **GPS Spoofing Prevention**:
   - Validate GPS accuracy
   - Check timestamp consistency
   - Monitor suspicious patterns

2. **QR Code Security**:
   - Use unique, unpredictable QR codes
   - Rotate codes periodically
   - Validate QR code is active and registered

3. **Data Privacy**:
   - GPS coordinates are stored
   - Implement data retention policy
   - Add GDPR compliance if needed

---

## 📞 Support

For issues or questions:
1. Check TROUBLESHOOTING.md
2. Review API documentation
3. Check Flask console for errors
4. Verify database tables created correctly

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Navigate to http://localhost:5000/attendance/
- [ ] Navigate to http://localhost:5000/qc/
- [ ] See "Attendance" and "QC Feedback" in navigation menu
- [ ] Attendance summary shows today's stats
- [ ] QC summary shows issue breakdown
- [ ] Can filter attendance records by date
- [ ] Can add new QC feedback
- [ ] Can view employee QC performance
- [ ] Database tables created: attendance_records, qc_feedback, work_sites
- [ ] Sample data loaded successfully

---

**Last Updated**: Now
**Version**: 1.0.0
**Compatible with**: Axis Ops Tracker v1.0.0
