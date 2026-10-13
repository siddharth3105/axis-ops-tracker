"""
Import Sample Data Script
Populates the database with sample employee data for testing
"""
import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Employee, Performance, Payment, Attendance

# Sample data
SUPERVISORS = ['Rishi', 'Manoj Patel', 'Arshid', 'Gobinda', 'Baba', 'Chandu', 'Vinod']
SHIFTS = ['Full Time', 'Day Shift', 'Night Shift']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
WORK_SITES = ['Site A', 'Site B', 'Site C', 'Site D']

def create_sample_employees(count=20):
    """Create sample employee records"""
    employees = []
    
    for i in range(1, count + 1):
        emp_id = f"AX{str(i).zfill(4)}"
        
        employee = Employee(
            employee_id=emp_id,
            name=f"Employee {i}",
            email=f"employee{i}@awign.com",
            mobile=f"9{random.randint(100000000, 999999999)}",
            shift=random.choice(SHIFTS),
            weekoff_day=random.choice(WEEKDAYS) if random.random() > 0.3 else None,
            supervisor=random.choice(SUPERVISORS),
            status='Active' if random.random() > 0.1 else 'Inactive',
            is_resident=random.choice([True, False]),
            is_supervisor=random.random() > 0.85,
            supervisor_email=f"{random.choice(SUPERVISORS).lower().replace(' ', '')}@awign.com",
            work_site=random.choice(WORK_SITES),
            date_of_joining=(datetime.now() - timedelta(days=random.randint(30, 730))).date(),
            accommodation='Provided' if random.random() > 0.5 else 'Self',
            accommodation_status='Active' if random.random() > 0.2 else 'Pending',
            training_date=(datetime.now() - timedelta(days=random.randint(1, 365))).date() if random.random() > 0.3 else None
        )
        
        employees.append(employee)
    
    return employees

def create_performance_data(employee):
    """Create performance data for an employee"""
    days_worked = (datetime.now().date() - employee.date_of_joining).days if employee.date_of_joining else 0
    
    performance = Performance(
        employee_id=employee.id,
        total_days_worked=days_worked,
        total_production_hours=round(random.uniform(100, 2000), 2),
        quality_percentage=round(random.uniform(70, 99), 2),
        total_videos=random.randint(50, 1000)
    )
    
    return performance

def create_payment_data(employee, count=3):
    """Create payment records for an employee"""
    payments = []
    
    for i in range(random.randint(1, count)):
        payment = Payment(
            employee_id=employee.id,
            payment_date=(datetime.now() - timedelta(days=random.randint(1, 180))).date(),
            hours_processed=round(random.uniform(40, 200), 2),
            amount_transferred=round(random.uniform(5000, 50000), 2),
            last_payment_date=(datetime.now() - timedelta(days=random.randint(1, 90))).date(),
            payment_status=random.choice(['Completed', 'Completed', 'Completed', 'Pending', 'Processing'])
        )
        payments.append(payment)
    
    return payments

def create_attendance_data(employee, days=30):
    """Create attendance records for an employee"""
    attendance_records = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).date()
        
        # Only create attendance if after joining date
        if employee.date_of_joining and date >= employee.date_of_joining:
            # 85% chance of being present
            if random.random() > 0.15:
                attendance = Attendance(
                    employee_id=employee.id,
                    date=date,
                    status='Present',
                    hours_worked=round(random.uniform(7, 10), 2),
                    notes=f"Regular work day"
                )
                attendance_records.append(attendance)
    
    return attendance_records

def main():
    """Main import function"""
    print("\n" + "="*60)
    print("AXIS OPS TRACKER - SAMPLE DATA IMPORT")
    print("="*60 + "\n")
    
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("🗑️  Clearing existing data...")
        Attendance.query.delete()
        Payment.query.delete()
        Performance.query.delete()
        Employee.query.delete()
        db.session.commit()
        print("✓ Existing data cleared\n")
        
        # Create employees
        print("👥 Creating sample employees...")
        employees = create_sample_employees(count=30)
        
        for employee in employees:
            db.session.add(employee)
        
        db.session.commit()
        print(f"✓ Created {len(employees)} employees\n")
        
        # Create performance, payment, and attendance data
        print("📊 Creating performance data...")
        print("💰 Creating payment records...")
        print("📅 Creating attendance records...")
        
        for employee in employees:
            # Performance
            performance = create_performance_data(employee)
            db.session.add(performance)
            
            # Payments
            payments = create_payment_data(employee)
            for payment in payments:
                db.session.add(payment)
            
            # Attendance
            attendance_records = create_attendance_data(employee, days=30)
            for attendance in attendance_records:
                db.session.add(attendance)
        
        db.session.commit()
        
        # Summary
        print("\n" + "="*60)
        print("✅ IMPORT COMPLETE!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Employees: {Employee.query.count()}")
        print(f"   • Active Employees: {Employee.query.filter_by(status='Active').count()}")
        print(f"   • Supervisors: {Employee.query.filter_by(is_supervisor=True).count()}")
        print(f"   • Performance Records: {Performance.query.count()}")
        print(f"   • Payment Records: {Payment.query.count()}")
        print(f"   • Attendance Records: {Attendance.query.count()}")
        print(f"\n🚀 Start the server with: python run.py")
        print(f"📊 Open dashboard at: http://localhost:5000\n")
        
        return 0

if __name__ == '__main__':
    sys.exit(main())
