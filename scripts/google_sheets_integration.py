"""
Google Sheets Integration Script
Fetches data from Google Sheets and syncs with database
"""
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Employee, Performance, Payment
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsSync:
    def __init__(self, spreadsheet_id, credentials_file='config/credentials.json'):
        """Initialize Google Sheets connection"""
        self.spreadsheet_id = spreadsheet_id
        self.credentials_file = credentials_file
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        self.client = None
        
    def connect(self):
        """Connect to Google Sheets"""
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, self.scope
            )
            self.client = gspread.authorize(creds)
            print("✓ Connected to Google Sheets")
            return True
        except Exception as e:
            print(f"✗ Error connecting to Google Sheets: {e}")
            return False
    
    def fetch_employee_data(self):
        """Fetch employee data from Google Sheets"""
        try:
            sheet = self.client.open_by_key(self.spreadsheet_id).sheet1
            data = sheet.get_all_records()
            print(f"✓ Fetched {len(data)} records from Google Sheets")
            return data
        except Exception as e:
            print(f"✗ Error fetching data: {e}")
            return []
    
    def parse_date(self, date_str):
        """Parse date from various formats"""
        if not date_str or date_str == '':
            return None
        
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%Y/%m/%d'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt).date()
            except:
                continue
        return None
    
    def sync_to_database(self, app):
        """Sync Google Sheets data to database"""
        if not self.connect():
            return False
        
        data = self.fetch_employee_data()
        if not data:
            return False
        
        with app.app_context():
            synced_count = 0
            updated_count = 0
            
            for row in data:
                try:
                    employee_id = row.get('Employee_ID', '').strip()
                    if not employee_id:
                        continue
                    
                    # Check if employee exists
                    employee = Employee.query.filter_by(employee_id=employee_id).first()
                    
                    if employee:
                        # Update existing employee
                        employee.name = row.get('Name', '')
                        employee.email = row.get('Awign Registered Gmail', '')
                        employee.mobile = row.get('Mobile number using in app', '')
                        employee.shift = row.get('Shift', '')
                        employee.weekoff_day = row.get('Weekoff_Day', '')
                        employee.supervisor = row.get('Supervisor', '')
                        employee.status = row.get('Status', 'Active')
                        employee.is_resident = str(row.get('Is_Resident', '')).lower() == 'yes'
                        employee.is_supervisor = str(row.get('Is_Supervisor', '')).lower() == 'true'
                        employee.supervisor_email = row.get('Supervisor email', '')
                        employee.work_site = row.get('Current_Work_Site', '')
                        employee.accommodation = row.get('Accomodation', '')
                        employee.accommodation_status = row.get('Accomodation Status', '')
                        
                        date_of_joining = self.parse_date(row.get('Date_Of_Joining', ''))
                        if date_of_joining:
                            employee.date_of_joining = date_of_joining
                        
                        training_date = self.parse_date(row.get('Training Date', ''))
                        if training_date:
                            employee.training_date = training_date
                        
                        updated_count += 1
                    else:
                        # Create new employee
                        employee = Employee(
                            employee_id=employee_id,
                            name=row.get('Name', ''),
                            email=row.get('Awign Registered Gmail', ''),
                            mobile=row.get('Mobile number using in app', ''),
                            shift=row.get('Shift', ''),
                            weekoff_day=row.get('Weekoff_Day', ''),
                            supervisor=row.get('Supervisor', ''),
                            status=row.get('Status', 'Active'),
                            is_resident=str(row.get('Is_Resident', '')).lower() == 'yes',
                            is_supervisor=str(row.get('Is_Supervisor', '')).lower() == 'true',
                            supervisor_email=row.get('Supervisor email', ''),
                            work_site=row.get('Current_Work_Site', ''),
                            date_of_joining=self.parse_date(row.get('Date_Of_Joining', '')),
                            accommodation=row.get('Accomodation', ''),
                            accommodation_status=row.get('Accomodation Status', ''),
                            training_date=self.parse_date(row.get('Training Date', '')),
                            user_id=row.get('User ID', '')
                        )
                        db.session.add(employee)
                        synced_count += 1
                    
                    # Sync performance data
                    performance = Performance.query.filter_by(employee_id=employee.id).first()
                    if not performance:
                        performance = Performance(employee_id=employee.id)
                        db.session.add(performance)
                    
                    performance.total_days_worked = int(row.get('Total Days Worked', 0) or 0)
                    performance.total_production_hours = float(row.get('Total Production (hrs)', 0) or 0)
                    performance.quality_percentage = float(row.get('Quality (%)', 0) or 0)
                    performance.total_videos = int(row.get('Total Videos', 0) or 0)
                    
                    # Sync payment data if available
                    amount_str = str(row.get('Total Amount Transferred (₹)', '')).replace('₹', '').replace(',', '').strip()
                    if amount_str and amount_str != '':
                        try:
                            amount = float(amount_str)
                            if amount > 0:
                                # Check if payment already exists
                                existing_payment = Payment.query.filter_by(
                                    employee_id=employee.id,
                                    amount_transferred=amount
                                ).first()
                                
                                if not existing_payment:
                                    payment = Payment(
                                        employee_id=employee.id,
                                        hours_processed=float(row.get('Hours Processed for Payment', 0) or 0),
                                        amount_transferred=amount,
                                        last_payment_date=self.parse_date(row.get('Last Payment Date', '')),
                                        payment_status='Completed'
                                    )
                                    db.session.add(payment)
                        except ValueError:
                            pass
                    
                except Exception as e:
                    print(f"✗ Error processing row {employee_id}: {e}")
                    continue
            
            try:
                db.session.commit()
                print(f"✓ Sync completed: {synced_count} new, {updated_count} updated")
                return True
            except Exception as e:
                db.session.rollback()
                print(f"✗ Error committing to database: {e}")
                return False


def main():
    """Main sync function"""
    # Your Google Spreadsheet ID
    SPREADSHEET_ID = '1L2lSDWKTQoApTlw-564RRupbO5SrFkinyoHLA_fd5yw'
    
    print("=" * 60)
    print("AXIS OPS TRACKER - GOOGLE SHEETS SYNC")
    print("=" * 60)
    
    app = create_app()
    sync = GoogleSheetsSync(SPREADSHEET_ID)
    
    success = sync.sync_to_database(app)
    
    if success:
        print("\n✓ Sync completed successfully!")
        return 0
    else:
        print("\n✗ Sync failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
