"""
Comprehensive automated test for Axis Ops Tracker.
Runs against a live Flask test client — no real server needed.
"""
import sys, json
sys.path.insert(0, r'c:\Users\SPURGE\AXIS AI TRACKER')

from app import create_app, db
from app.models import Employee, Performance, Payment, Attendance, AttendanceRecord, QCFeedback, WorkSite
from datetime import date, datetime

app = create_app()

PASS = []
FAIL = []

def check(name, condition, detail=""):
    if condition:
        PASS.append(name)
        print(f"  [PASS] {name}")
    else:
        FAIL.append(name)
        print(f"  [FAIL] {name}" + (f" — {detail}" if detail else ""))

def jget(client, url):
    r = client.get(url)
    try:    return r.status_code, r.get_json()
    except: return r.status_code, {}

def jpost(client, url, body):
    r = client.post(url, json=body, content_type='application/json')
    try:    return r.status_code, r.get_json()
    except: return r.status_code, {}

def jput(client, url, body):
    r = client.put(url, json=body, content_type='application/json')
    try:    return r.status_code, r.get_json()
    except: return r.status_code, {}

def jdelete(client, url):
    r = client.delete(url)
    try:    return r.status_code, r.get_json()
    except: return r.status_code, {}

with app.test_client() as c:
    with app.app_context():
        # ── Reset to a known empty state ──────────────────────────────────
        db.drop_all()
        db.create_all()
        print("\n══════════════════════════════════════════")
        print("  AXIS OPS TRACKER — FULL TEST SUITE")
        print("══════════════════════════════════════════\n")

        # ── 1. PAGE ROUTES ────────────────────────────────────────────────
        print("── 1. Page routes (HTML) ─────────────────")
        for path in ['/', '/employees/', '/attendance/', '/qc/', '/analytics/', '/payments/', '/reports/']:
            st, _ = jget(c, path)
            check(f"GET {path} → 200", st == 200)

        # ── 2. DASHBOARD API ──────────────────────────────────────────────
        print("\n── 2. Dashboard API ──────────────────────")
        st, d = jget(c, '/api/dashboard/stats')
        check("Dashboard stats returns success", st == 200 and d.get('success'))
        check("Dashboard stats has employees key", 'stats' in d and 'employees' in d.get('stats', {}))

        st, d = jget(c, '/api/dashboard/recent-activity')
        check("Dashboard recent-activity returns success", st == 200 and d.get('success'))

        # ── 3. EMPLOYEE CRUD ──────────────────────────────────────────────
        print("\n── 3. Employee CRUD ──────────────────────")
        st, d = jpost(c, '/employees/api/create', {
            'employee_id': 'EMP001', 'name': 'Alice Kumar',
            'email': 'alice@axis.com', 'mobile': '9876543210',
            'shift': 'Day Shift', 'weekoff_day': 'Sunday',
            'supervisor': 'Bob Sharma', 'status': 'Active',
            'is_resident': True, 'is_supervisor': False,
            'work_site': 'Site A', 'date_of_joining': '2024-01-15'
        })
        check("Create employee → 201", st == 201 and d.get('success'))
        emp_id = d.get('employee', {}).get('id')
        check("Employee id returned", bool(emp_id))

        st, d = jpost(c, '/employees/api/create', {
            'employee_id': 'EMP002', 'name': 'Bob Sharma',
            'email': 'bob@axis.com', 'shift': 'Night Shift',
            'status': 'Active', 'is_supervisor': True
        })
        check("Create second employee → 201", st == 201 and d.get('success'))
        emp2_id = d.get('employee', {}).get('id')

        st, d = jpost(c, '/employees/api/create', {'employee_id': 'EMP001', 'name': 'Dup', 'email': 'dup@axis.com'})
        check("Duplicate employee_id → 400", st == 400 and not d.get('success'))

        st, d = jget(c, '/employees/api/list')
        check("List employees returns 2", st == 200 and d.get('count') == 2)

        st, d = jget(c, '/employees/api/list?status=Active')
        check("Filter by status Active", st == 200 and d.get('success'))

        st, d = jget(c, '/employees/api/list?search=alice')
        check("Search employees by name", st == 200 and len(d.get('employees', [])) == 1)

        st, d = jget(c, f'/employees/api/{emp_id}')
        check("Get single employee", st == 200 and d.get('employee', {}).get('name') == 'Alice Kumar')

        st, d = jput(c, f'/employees/api/{emp_id}/update', {'mobile': '1111111111'})
        check("Update employee", st == 200 and d.get('success'))

        st, d = jget(c, '/employees/api/filters')
        check("Get filters (supervisors/shifts)", st == 200 and d.get('success'))

        # ── 4. PAYMENTS ───────────────────────────────────────────────────
        print("\n── 4. Payments ───────────────────────────")
        st, d = jpost(c, '/payments/api/create', {
            'employee_id': emp_id, 'payment_date': '2024-06-01',
            'hours_processed': 160.0, 'amount_transferred': 25000.0,
            'payment_status': 'Completed'
        })
        check("Create payment → 201", st == 201 and d.get('success'))
        pay_id = d.get('payment', {}).get('id')

        st, d = jpost(c, '/payments/api/create', {
            'employee_id': emp_id, 'payment_date': '2024-07-01',
            'hours_processed': 80.0, 'amount_transferred': 12000.0,
            'payment_status': 'Pending'
        })
        check("Create second payment → 201", st == 201 and d.get('success'))

        st, d = jget(c, '/payments/api/list')
        check("List payments", st == 200 and d.get('count') == 2)

        st, d = jget(c, '/payments/api/list?status=Pending')
        check("Filter payments by Pending", st == 200 and d.get('count') == 1)

        # NEW: single-payment GET endpoint
        st, d = jget(c, f'/payments/api/{pay_id}')
        check("GET single payment endpoint works", st == 200 and d.get('success') and d.get('payment', {}).get('id') == pay_id)
        check("Single payment has employee_id", 'employee_id' in d.get('payment', {}))

        st, d = jget(c, '/payments/api/summary')
        check("Payment summary", st == 200 and d.get('success'))
        check("Payment summary total_paid correct", d.get('summary', {}).get('total_paid') == 25000.0)

        st, d = jput(c, f'/payments/api/{pay_id}/update', {'payment_status': 'Processing'})
        check("Update payment status", st == 200 and d.get('success'))

        st, d = jget(c, f'/payments/api/employee/{emp_id}')
        check("Employee payments", st == 200 and d.get('success'))

        # ── 5. ATTENDANCE (legacy model) ──────────────────────────────────
        print("\n── 5. Attendance (legacy) ────────────────")
        with app.app_context():
            att = Attendance(employee_id=emp_id, date=date(2024, 6, 10),
                             status='Present', hours_worked=8.0)
            db.session.add(att)
            db.session.commit()

        st, d = jget(c, f'/employees/api/{emp_id}')
        check("Employee detail includes attendance array", isinstance(d.get('attendance'), list))

        # ── 6. ATTENDANCE TRACKING (QR model) ─────────────────────────────
        print("\n── 6. Attendance Tracking (QR) ───────────")
        with app.app_context():
            site = WorkSite(site_id='SITE001', site_name='Main Office',
                            latitude=12.9716, longitude=77.5946,
                            allowed_radius_meters=200, gps_accuracy_limit_meters=100,
                            is_active=True, qr_code_data='QR_SITE001')
            db.session.add(site)
            db.session.commit()

        st, d = jget(c, '/attendance/api/summary')
        check("Attendance summary", st == 200 and d.get('success'))

        st, d = jget(c, '/attendance/api/work-sites')
        check("List work sites", st == 200 and len(d.get('work_sites', [])) == 1)

        st, d = jget(c, f'/attendance/api/today-status/{emp_id}')
        check("Today status for employee", st == 200 and d.get('success'))

        # Manual add endpoint (NEW)
        st, d = jpost(c, '/attendance/api/add-manual', {
            'employee_id': emp_id,
            'attendance_date': str(date.today()),
            'check_in_time': '09:00',
            'check_out_time': '17:00',
            'status': 'Checked Out',
            'work_site_id': 'SITE001'
        })
        check("Manual attendance add → 201", st == 201 and d.get('success'))
        att_record_id = d.get('attendance', {}).get('id')
        check("Manual attendance has hours_worked", d.get('attendance', {}).get('hours_worked') == 8.0)

        st, d = jget(c, '/attendance/api/list')
        check("List attendance records", st == 200 and d.get('count') >= 1)

        # Edit via add-manual with id
        st, d = jpost(c, '/attendance/api/add-manual', {
            'id': att_record_id,
            'employee_id': emp_id,
            'attendance_date': str(date.today()),
            'check_in_time': '08:00',
            'check_out_time': '16:00',
            'status': 'Checked Out',
        })
        check("Manual attendance edit → 201", st == 201 and d.get('success'))
        check("Edit updates hours_worked to 8.0", d.get('attendance', {}).get('hours_worked') == 8.0)

        # Delete endpoint (NEW)
        st, d = jdelete(c, f'/attendance/api/{att_record_id}/delete')
        check("Delete attendance record", st == 200 and d.get('success'))

        st, d = jget(c, '/attendance/api/list')
        check("Record removed after delete", d.get('count') == 0)

        # ── 7. QC FEEDBACK ────────────────────────────────────────────────
        print("\n── 7. QC Feedback ────────────────────────")
        st, d = jpost(c, '/qc/api/submit', {
            'employee_id': emp_id,
            'video_id': 'VID001',
            'task_name': 'Folding Clothes',
            'video_duration': 12.5,
            'recorded_date': '2024-06-01',
            'qc_status': 'Approved',
            'approval_percentage': 95.0,
            'poor_lighting': False,
            'shaky_camera': True,
            'qc_reviewer': 'QC Team',
            'qc_comments': 'Good work but camera was shaky'
        })
        check("Submit QC feedback → 201", st == 201 and d.get('success'))
        qc_id = d.get('feedback', {}).get('id')

        st, d = jpost(c, '/qc/api/submit', {
            'employee_id': emp_id,
            'task_name': 'Washing Dishes',
            'video_duration': 8.0,
            'recorded_date': '2024-06-02',
            'qc_status': 'Rejected',
            'approval_percentage': 30.0,
            'blurry_video': True,
            'hands_not_visible': True,
            'qc_reviewer': 'QC Team'
        })
        check("Submit second QC feedback (Rejected) → 201", st == 201 and d.get('success'))

        st, d = jget(c, '/qc/api/list')
        check("List QC feedback", st == 200 and d.get('count') == 2)

        st, d = jget(c, '/qc/api/list?status=Approved')
        check("Filter QC by Approved", st == 200 and d.get('count') == 1)

        # Single feedback GET (used by viewDetails and editFeedback)
        st, d = jget(c, f'/qc/api/{qc_id}')
        check("GET single QC feedback", st == 200 and d.get('success'))
        check("Single feedback has issues dict", isinstance(d.get('feedback', {}).get('issues'), dict))
        check("Single feedback has employee_name", 'employee_name' in d.get('feedback', {}))
        check("Single feedback shaky_camera is True", d.get('feedback', {}).get('issues', {}).get('shaky_camera') is True)

        st, d = jput(c, f'/qc/api/{qc_id}/update', {
            'qc_status': 'Trimmed',
            'approval_percentage': 80.0,
            'qc_comments': 'Updated after trim'
        })
        check("Update QC feedback", st == 200 and d.get('success'))
        check("QC status updated to Trimmed", d.get('feedback', {}).get('qc_status') == 'Trimmed')

        st, d = jget(c, '/qc/api/summary')
        check("QC summary returns success", st == 200 and d.get('success'))
        check("QC summary has status_breakdown", 'status_breakdown' in d.get('summary', {}))
        check("QC summary has top_issues", 'top_issues' in d.get('summary', {}))

        st, d = jget(c, f'/qc/api/employee/{emp_id}/stats')
        check("Employee QC stats", st == 200 and d.get('success'))
        check("QC stats total_videos == 2", d.get('stats', {}).get('total_videos') == 2)

        # ── 8. ANALYTICS ─────────────────────────────────────────────────
        print("\n── 8. Analytics ──────────────────────────")
        st, d = jget(c, '/analytics/api/performance/overview')
        check("Performance overview", st == 200 and d.get('success'))

        st, d = jget(c, '/analytics/api/attendance/summary')
        check("Attendance summary (analytics)", st == 200 and d.get('success'))

        st, d = jget(c, '/analytics/api/trends')
        check("Trends endpoint", st == 200 and d.get('success'))

        # Performance update endpoint (NEW)
        st, d = jpost(c, '/analytics/api/performance/update', {
            'employee_id': emp_id,
            'total_days_worked': 22,
            'total_production_hours': 176.0,
            'quality_percentage': 94.5,
            'total_videos': 45
        })
        check("Performance update endpoint", st == 200 and d.get('success'))
        check("Performance quality stored correctly",
              d.get('performance', {}).get('quality_percentage') == 94.5)

        # ── 9. REPORTS ────────────────────────────────────────────────────
        print("\n── 9. Reports ────────────────────────────")
        st, d = jget(c, '/reports/api/generate/employee-roster')
        check("Generate employee roster CSV", st == 200 and d.get('success'))
        check("Employee roster has CSV data", bool(d.get('data')))
        check("Employee roster filename ends .csv", str(d.get('filename', '')).endswith('.csv'))

        st, d = jget(c, '/reports/api/generate/performance-report')
        check("Generate performance report CSV", st == 200 and d.get('success'))

        st, d = jget(c, '/reports/api/generate/payment-report')
        check("Generate payment report CSV", st == 200 and d.get('success'))

        st, d = jget(c, '/reports/api/generate/payment-report?start_date=2024-06-01&end_date=2024-06-30')
        check("Generate payment report with date range", st == 200 and d.get('success'))

        st, d = jget(c, '/reports/api/generate/supervisor-report')
        check("Generate supervisor report CSV", st == 200 and d.get('success'))

        # ── 10. QR CHECK-IN (requires GPS + valid QR) ─────────────────────
        print("\n── 10. QR Check-in / Check-out ───────────")
        st, d = jpost(c, '/attendance/api/check-in', {
            'employee_id': emp_id,
            'qr_code': 'QR_SITE001',
            'latitude': 12.9716,
            'longitude': 77.5946,
            'accuracy': 10.0
        })
        check("QR check-in succeeds", st == 201 and d.get('success'))
        check("Check-in returns check_in_time", bool(d.get('check_in_time')))

        # Scan again immediately → should block (< 5 min)
        st, d2 = jpost(c, '/attendance/api/check-in', {
            'employee_id': emp_id,
            'qr_code': 'QR_SITE001',
            'latitude': 12.9716,
            'longitude': 77.5946,
            'accuracy': 10.0
        })
        check("Immediate re-scan blocked", st == 400 and not d2.get('success'))

        # QR with bad GPS accuracy
        st, d3 = jpost(c, '/attendance/api/check-in', {
            'employee_id': emp2_id,
            'qr_code': 'QR_SITE001',
            'latitude': 12.9716, 'longitude': 77.5946,
            'accuracy': 999.0
        })
        check("Bad GPS accuracy rejected", st == 400 and not d3.get('success'))

        # QR with wrong code
        st, d4 = jpost(c, '/attendance/api/check-in', {
            'employee_id': emp2_id,
            'qr_code': 'INVALID_QR',
            'latitude': 12.9716, 'longitude': 77.5946,
            'accuracy': 10.0
        })
        check("Invalid QR code rejected", st == 400 and not d4.get('success'))

        # ── 11. EMPLOYEE DELETE ────────────────────────────────────────────
        print("\n── 11. Employee delete / cascade ─────────")
        # Create a disposable employee to delete
        st, d = jpost(c, '/employees/api/create', {
            'employee_id': 'EMP999', 'name': 'Temp Employee',
            'email': 'temp@axis.com', 'status': 'Inactive'
        })
        tmp_id = d.get('employee', {}).get('id')
        st, d = jdelete(c, f'/employees/api/{tmp_id}/delete')
        check("Delete employee", st == 200 and d.get('success'))

        st, d = jget(c, '/employees/api/list')
        check("Employee count back to 2 after delete", d.get('count') == 2)

        # ── SUMMARY ───────────────────────────────────────────────────────
        print("\n══════════════════════════════════════════")
        total = len(PASS) + len(FAIL)
        print(f"  RESULTS:  {len(PASS)} passed / {len(FAIL)} failed / {total} total")
        if FAIL:
            print("\n  FAILED TESTS:")
            for f in FAIL:
                print(f"    ✗ {f}")
        else:
            print("\n  All tests passed!")
        print("══════════════════════════════════════════\n")
        sys.exit(0 if not FAIL else 1)
