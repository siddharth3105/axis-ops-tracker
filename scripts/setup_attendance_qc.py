"""
Setup Attendance and QC Features
Creates new database tables and adds sample data
"""
import os
import sys
from datetime import datetime, timedelta, date
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Employee, AttendanceRecord, QCFeedback, WorkSite

# Sample work sites
WORK_SITES = [
    {'site_id': 'SITE_A', 'site_name': 'Main Office', 'lat': 28.6139, 'lon': 77.2090},
    {'site_id': 'SITE_B', 'site_name': 'Production Floor A', 'lat': 28.6150, 'lon': 77.2100},
    {'site_id': 'SITE_C', 'site_name': 'Production Floor B', 'lat': 28.6160, 'lon': 77.2110},
    {'site_id': 'SITE_D', 'site_name': 'Warehouse', 'lat': 28.6170, 'lon': 77.2120}
]

# Sample tasks for QC
TASKS = [
    'Folding Clothes', 'Washing Dishes', 'Cleaning Kitchen', 'Ironing Clothes',
    'Organizing Shelves', 'Mopping Floor', 'Dusting Furniture', 'Window Cleaning',
    'Laundry Sorting', 'Bed Making', 'Vacuuming Carpet', 'Polishing Silverware'
]

QC_STATUSES = ['Approved', 'Rejected', 'Pending', 'Trimmed']


def create_tables():
    """Create new database tables"""
    print("🔨 Creating database tables...")
    db.create_all()
    print("✓ Tables created\n")


def setup_work_sites():
    """Create work site locations"""
    print("📍 Setting up work sites...")
    
    for site_data in WORK_SITES:
        existing = WorkSite.query.filter_by(site_id=site_data['site_id']).first()
        if existing:
            print(f"   • {site_data['site_name']} already exists")
            continue
        
        work_site = WorkSite(
            site_id=site_data['site_id'],
            site_name=site_data['site_name'],
            latitude=site_data['lat'],
            longitude=site_data['lon'],
            allowed_radius_meters=150,
            gps_accuracy_limit_meters=100,
            is_active=True,
            qr_code_data=f"QR_{site_data['site_id']}_{random.randint(1000, 9999)}"
        )
        db.session.add(work_site)
        print(f"   ✓ Created work site: {site_data['site_name']}")
    
    db.session.commit()
    print(f"✓ Created {len(WORK_SITES)} work sites\n")


def create_attendance_data(days=30):
    """Create sample attendance records"""
    print(f"📅 Creating attendance data for last {days} days...")
    
    employees = Employee.query.filter_by(status='Active').all()
    work_sites = WorkSite.query.all()
    
    if not employees:
        print("   ⚠ No employees found. Run import_sample_data.py first")
        return
    
    if not work_sites:
        print("   ⚠ No work sites found")
        return
    
    count = 0
    for day_offset in range(days):
        attendance_date = date.today() - timedelta(days=day_offset)
        
        # 85% of employees mark attendance each day
        attending_employees = random.sample(employees, int(len(employees) * 0.85))
        
        for emp in attending_employees:
            # Skip if attendance already exists
            existing = AttendanceRecord.query.filter_by(
                employee_id=emp.id,
                attendance_date=attendance_date
            ).first()
            
            if existing:
                continue
            
            work_site = random.choice(work_sites)
            
            # Random check-in time (7 AM to 10 AM)
            check_in_hour = random.randint(7, 10)
            check_in_minute = random.randint(0, 59)
            check_in_time = datetime.combine(attendance_date, datetime.min.time()) + \
                          timedelta(hours=check_in_hour, minutes=check_in_minute)
            
            # Check-out time (5 PM to 8 PM for non-residents)
            check_out_time = None
            hours_worked = None
            status = 'Checked In'
            
            if not emp.is_resident and attendance_date < date.today():
                check_out_hour = random.randint(17, 20)
                check_out_minute = random.randint(0, 59)
                check_out_time = datetime.combine(attendance_date, datetime.min.time()) + \
                               timedelta(hours=check_out_hour, minutes=check_out_minute)
                hours_worked = (check_out_time - check_in_time).total_seconds() / 3600
                status = 'Checked Out'
            
            # Random GPS coordinates near work site (within 50m)
            lat_offset = random.uniform(-0.0005, 0.0005)
            lon_offset = random.uniform(-0.0005, 0.0005)
            
            attendance = AttendanceRecord(
                employee_id=emp.id,
                attendance_date=attendance_date,
                check_in_time=check_in_time,
                check_out_time=check_out_time,
                check_in_latitude=work_site.latitude + lat_offset,
                check_in_longitude=work_site.longitude + lon_offset,
                check_in_accuracy=random.uniform(10, 50),
                work_site_id=work_site.site_id,
                qr_code_scanned=work_site.qr_code_data,
                status=status,
                hours_worked=hours_worked,
                is_valid=True
            )
            
            db.session.add(attendance)
            count += 1
            
            if count % 50 == 0:
                db.session.commit()
                print(f"   • Created {count} attendance records...")
    
    db.session.commit()
    print(f"✓ Created {count} attendance records\n")


def create_qc_feedback_data(count=100):
    """Create sample QC feedback records"""
    print(f"📹 Creating {count} QC feedback records...")
    
    employees = Employee.query.filter_by(status='Active').all()
    
    if not employees:
        print("   ⚠ No employees found")
        return
    
    created = 0
    for i in range(count):
        emp = random.choice(employees)
        recorded_date = date.today() - timedelta(days=random.randint(0, 60))
        
        # Random status with weights
        status_choice = random.choices(
            QC_STATUSES,
            weights=[60, 20, 10, 10]  # More approved than rejected
        )[0]
        
        # Approval percentage based on status
        if status_choice == 'Approved':
            approval_pct = random.uniform(80, 100)
        elif status_choice == 'Rejected':
            approval_pct = random.uniform(0, 50)
        else:
            approval_pct = random.uniform(50, 80)
        
        # Random issues (more likely if rejected)
        has_issues = status_choice == 'Rejected'
        
        feedback = QCFeedback(
            employee_id=emp.id,
            video_id=f"VID_{emp.employee_id}_{random.randint(1000, 9999)}",
            task_name=random.choice(TASKS),
            video_duration=round(random.uniform(2, 10), 2),
            recorded_date=recorded_date,
            qc_status=status_choice,
            approval_percentage=round(approval_pct, 2),
            
            # Issues (more common if rejected)
            wrist_camera_mismatch=has_issues and random.random() > 0.7,
            hands_not_visible=has_issues and random.random() > 0.8,
            poor_lighting=has_issues and random.random() > 0.7,
            wrong_environment=has_issues and random.random() > 0.9,
            shaky_camera=has_issues and random.random() > 0.8,
            video_too_short=has_issues and random.random() > 0.9,
            blurry_video=has_issues and random.random() > 0.75,
            task_too_slow=has_issues and random.random() > 0.7,
            irrelevant_video=has_issues and random.random() > 0.95,
            pretending_working=has_issues and random.random() > 0.9,
            
            qc_reviewer='QC Team' if status_choice != 'Pending' else None,
            reviewed_date=datetime.now() if status_choice != 'Pending' else None
        )
        
        db.session.add(feedback)
        created += 1
        
        if created % 25 == 0:
            db.session.commit()
            print(f"   • Created {created} QC feedback records...")
    
    db.session.commit()
    print(f"✓ Created {created} QC feedback records\n")


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("AXIS OPS TRACKER - ATTENDANCE & QC SETUP")
    print("="*60 + "\n")
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        create_tables()
        
        # Setup work sites
        setup_work_sites()
        
        # Create sample data
        create_attendance_data(days=30)
        create_qc_feedback_data(count=100)
        
        # Summary
        print("="*60)
        print("✅ SETUP COMPLETE!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Work Sites: {WorkSite.query.count()}")
        print(f"   • Attendance Records: {AttendanceRecord.query.count()}")
        print(f"   • QC Feedback: {QCFeedback.query.count()}")
        print(f"\n🚀 Start the server with: python run.py")
        print(f"📊 Access new features:")
        print(f"   • Attendance: http://localhost:5000/attendance/")
        print(f"   • QC Feedback: http://localhost:5000/qc/\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
