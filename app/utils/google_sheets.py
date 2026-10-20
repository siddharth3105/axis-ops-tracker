"""
Google Sheets Integration
Syncs data between Axis Ops Tracker and Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import os


class GoogleSheetsSync:
    """Handle Google Sheets synchronization"""
    
    # Your spreadsheet URL
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw/edit?usp=sharing"
    SPREADSHEET_ID = "1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw"
    
    # Required Google API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.credentials_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'config',
            'credentials.json'
        )
    
    def connect(self):
        """Connect to Google Sheets API"""
        try:
            if not os.path.exists(self.credentials_path):
                raise FileNotFoundError(
                    f"Google credentials not found at {self.credentials_path}\n"
                    f"Please follow the setup instructions in GOOGLE_SHEETS_SETUP.md"
                )
            
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            
            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(self.SPREADSHEET_ID)
            
            return True
        except Exception as e:
            print(f"Error connecting to Google Sheets: {str(e)}")
            return False
    
    def sync_employees(self, employees):
        """Sync employees to Google Sheet"""
        if not self.client:
            if not self.connect():
                return {'success': False, 'error': 'Failed to connect to Google Sheets'}
        
        try:
            # Get or create 'Employees' worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Employees')
            except:
                worksheet = self.spreadsheet.add_worksheet('Employees', 1000, 20)
            
            # Clear existing data
            worksheet.clear()
            
            # Headers
            headers = [
                'Employee ID', 'Name', 'Email', 'Mobile', 'Shift',
                'Weekoff Day', 'Supervisor', 'Status', 'Is Resident',
                'Is Supervisor', 'Work Site', 'Date of Joining',
                'Accommodation', 'Accommodation Status', 'Training Date',
                'Created At'
            ]
            
            # Prepare data rows
            rows = [headers]
            for emp in employees:
                rows.append([
                    emp.employee_id,
                    emp.name,
                    emp.email,
                    emp.mobile or '',
                    emp.shift or '',
                    emp.weekoff_day or '',
                    emp.supervisor or '',
                    emp.status or 'Active',
                    'Yes' if emp.is_resident else 'No',
                    'Yes' if emp.is_supervisor else 'No',
                    emp.work_site or '',
                    emp.date_of_joining.isoformat() if emp.date_of_joining else '',
                    emp.accommodation or '',
                    emp.accommodation_status or '',
                    emp.training_date.isoformat() if emp.training_date else '',
                    emp.created_at.isoformat() if emp.created_at else ''
                ])
            
            # Update worksheet
            worksheet.update('A1', rows)
            
            # Format headers
            worksheet.format('A1:P1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9}
            })
            
            return {
                'success': True,
                'message': f'Synced {len(employees)} employees to Google Sheets',
                'count': len(employees)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def sync_attendance(self, attendance_records):
        """Sync attendance records to Google Sheet"""
        if not self.client:
            if not self.connect():
                return {'success': False, 'error': 'Failed to connect to Google Sheets'}
        
        try:
            # Get or create 'Attendance' worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Attendance')
            except:
                worksheet = self.spreadsheet.add_worksheet('Attendance', 1000, 15)
            
            # Clear existing data
            worksheet.clear()
            
            # Headers
            headers = [
                'Date', 'Employee ID', 'Employee Name', 'Check In Time',
                'Check Out Time', 'Hours Worked', 'Work Site', 'Status',
                'Check In Lat', 'Check In Lon', 'GPS Accuracy',
                'Is Valid', 'Validation Message'
            ]
            
            # Prepare data rows
            rows = [headers]
            for record, emp_name, emp_code in attendance_records:
                rows.append([
                    record.attendance_date.isoformat() if record.attendance_date else '',
                    emp_code,
                    emp_name,
                    record.check_in_time.strftime('%H:%M:%S') if record.check_in_time else '',
                    record.check_out_time.strftime('%H:%M:%S') if record.check_out_time else '',
                    round(record.hours_worked or 0, 2),
                    record.work_site_id or '',
                    record.status or '',
                    round(record.check_in_latitude or 0, 6),
                    round(record.check_in_longitude or 0, 6),
                    round(record.check_in_accuracy or 0, 2),
                    'Yes' if record.is_valid else 'No',
                    record.validation_message or ''
                ])
            
            # Update worksheet
            worksheet.update('A1', rows)
            
            # Format headers
            worksheet.format('A1:M1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.3, 'green': 0.7, 'blue': 0.3}
            })
            
            return {
                'success': True,
                'message': f'Synced {len(attendance_records)} attendance records to Google Sheets',
                'count': len(attendance_records)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def sync_qc_feedback(self, qc_records):
        """Sync QC feedback to Google Sheet"""
        if not self.client:
            if not self.connect():
                return {'success': False, 'error': 'Failed to connect to Google Sheets'}
        
        try:
            # Get or create 'QC Feedback' worksheet
            try:
                worksheet = self.spreadsheet.worksheet('QC Feedback')
            except:
                worksheet = self.spreadsheet.add_worksheet('QC Feedback', 1000, 25)
            
            # Clear existing data
            worksheet.clear()
            
            # Headers
            headers = [
                'Submitted Date', 'Employee ID', 'Employee Name', 'Video ID',
                'Task Name', 'Duration (min)', 'Status', 'Approval %',
                'Wrist Camera Issue', 'Hands Not Visible', 'Poor Lighting',
                'Wrong Environment', 'Shaky Camera', 'Video Too Short',
                'Blurry Video', 'Task Too Slow', 'Irrelevant Video',
                'Pretending', 'QC Reviewer', 'Comments', 'Reviewed Date'
            ]
            
            # Prepare data rows
            rows = [headers]
            for qc, emp_name, emp_code in qc_records:
                rows.append([
                    qc.submitted_date.strftime('%Y-%m-%d %H:%M') if qc.submitted_date else '',
                    emp_code,
                    emp_name,
                    qc.video_id or '',
                    qc.task_name or '',
                    round(qc.video_duration or 0, 2),
                    qc.qc_status or '',
                    round(qc.approval_percentage or 0, 1),
                    'Yes' if qc.wrist_camera_mismatch or qc.wrist_camera_not_worn else 'No',
                    'Yes' if qc.hands_not_visible else 'No',
                    'Yes' if qc.poor_lighting else 'No',
                    'Yes' if qc.wrong_environment else 'No',
                    'Yes' if qc.shaky_camera else 'No',
                    'Yes' if qc.video_too_short else 'No',
                    'Yes' if qc.blurry_video else 'No',
                    'Yes' if qc.task_too_slow else 'No',
                    'Yes' if qc.irrelevant_video else 'No',
                    'Yes' if qc.pretending_working else 'No',
                    qc.qc_reviewer or '',
                    qc.qc_comments or '',
                    qc.reviewed_date.strftime('%Y-%m-%d %H:%M') if qc.reviewed_date else ''
                ])
            
            # Update worksheet
            worksheet.update('A1', rows)
            
            # Format headers
            worksheet.format('A1:U1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.5, 'blue': 0.2}
            })
            
            return {
                'success': True,
                'message': f'Synced {len(qc_records)} QC feedback records to Google Sheets',
                'count': len(qc_records)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def sync_performance(self, performance_data):
        """Sync performance data to Google Sheet"""
        if not self.client:
            if not self.connect():
                return {'success': False, 'error': 'Failed to connect to Google Sheets'}
        
        try:
            # Get or create 'Performance' worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Performance')
            except:
                worksheet = self.spreadsheet.add_worksheet('Performance', 1000, 10)
            
            # Clear existing data
            worksheet.clear()
            
            # Headers
            headers = [
                'Employee ID', 'Employee Name', 'Total Days Worked',
                'Total Production Hours', 'Quality %', 'Total Videos',
                'Last Updated'
            ]
            
            # Prepare data rows
            rows = [headers]
            for perf, emp_name, emp_code in performance_data:
                rows.append([
                    emp_code,
                    emp_name,
                    perf.total_days_worked or 0,
                    round(perf.total_production_hours or 0, 2),
                    round(perf.quality_percentage or 0, 2),
                    perf.total_videos or 0,
                    perf.recorded_date.isoformat() if perf.recorded_date else ''
                ])
            
            # Update worksheet
            worksheet.update('A1', rows)
            
            # Format headers
            worksheet.format('A1:G1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.6, 'green': 0.3, 'blue': 0.8}
            })
            
            return {
                'success': True,
                'message': f'Synced {len(performance_data)} performance records to Google Sheets',
                'count': len(performance_data)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def sync_payments(self, payments):
        """Sync payment data to Google Sheet"""
        if not self.client:
            if not self.connect():
                return {'success': False, 'error': 'Failed to connect to Google Sheets'}
        
        try:
            # Get or create 'Payments' worksheet
            try:
                worksheet = self.spreadsheet.worksheet('Payments')
            except:
                worksheet = self.spreadsheet.add_worksheet('Payments', 1000, 10)
            
            # Clear existing data
            worksheet.clear()
            
            # Headers
            headers = [
                'Payment Date', 'Employee ID', 'Employee Name',
                'Hours Processed', 'Amount Transferred (₹)', 'Payment Status',
                'Last Payment Date', 'Created At'
            ]
            
            # Prepare data rows
            rows = [headers]
            for pay, emp_name, emp_code in payments:
                rows.append([
                    pay.payment_date.isoformat() if pay.payment_date else '',
                    emp_code,
                    emp_name,
                    round(pay.hours_processed or 0, 2),
                    round(pay.amount_transferred or 0, 2),
                    pay.payment_status or '',
                    pay.last_payment_date.isoformat() if pay.last_payment_date else '',
                    pay.created_at.isoformat() if pay.created_at else ''
                ])
            
            # Update worksheet
            worksheet.update('A1', rows)
            
            # Format headers
            worksheet.format('A1:H1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.2, 'green': 0.8, 'blue': 0.6}
            })
            
            return {
                'success': True,
                'message': f'Synced {len(payments)} payment records to Google Sheets',
                'count': len(payments)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def sync_all(self):
        """Sync all data to Google Sheets"""
        from app.models import Employee, AttendanceRecord, QCFeedback, Performance, Payment
        from app import db
        
        results = {
            'success': True,
            'synced': [],
            'errors': []
        }
        
        try:
            # Sync Employees
            employees = Employee.query.all()
            result = self.sync_employees(employees)
            if result['success']:
                results['synced'].append(f"Employees: {result['count']}")
            else:
                results['errors'].append(f"Employees: {result['error']}")
            
            # Sync Attendance
            attendance = db.session.query(
                AttendanceRecord,
                Employee.name,
                Employee.employee_id
            ).join(Employee, Employee.id == AttendanceRecord.employee_id).all()
            
            result = self.sync_attendance(attendance)
            if result['success']:
                results['synced'].append(f"Attendance: {result['count']}")
            else:
                results['errors'].append(f"Attendance: {result['error']}")
            
            # Sync QC Feedback
            qc_records = db.session.query(
                QCFeedback,
                Employee.name,
                Employee.employee_id
            ).join(Employee, Employee.id == QCFeedback.employee_id).all()
            
            result = self.sync_qc_feedback(qc_records)
            if result['success']:
                results['synced'].append(f"QC Feedback: {result['count']}")
            else:
                results['errors'].append(f"QC Feedback: {result['error']}")
            
            # Sync Performance
            performance = db.session.query(
                Performance,
                Employee.name,
                Employee.employee_id
            ).join(Employee, Employee.id == Performance.employee_id).all()
            
            result = self.sync_performance(performance)
            if result['success']:
                results['synced'].append(f"Performance: {result['count']}")
            else:
                results['errors'].append(f"Performance: {result['error']}")
            
            # Sync Payments
            payments = db.session.query(
                Payment,
                Employee.name,
                Employee.employee_id
            ).join(Employee, Employee.id == Payment.employee_id).all()
            
            result = self.sync_payments(payments)
            if result['success']:
                results['synced'].append(f"Payments: {result['count']}")
            else:
                results['errors'].append(f"Payments: {result['error']}")
            
            if results['errors']:
                results['success'] = False
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'synced': results['synced'],
                'errors': results['errors']
            }
