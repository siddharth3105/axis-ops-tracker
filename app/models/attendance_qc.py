"""
Attendance and QC Models
"""
from app import db
from datetime import datetime


class AttendanceRecord(db.Model):
    """QR-based attendance tracking"""
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Check-in/Check-out
    check_in_time = db.Column(db.DateTime, nullable=False)
    check_out_time = db.Column(db.DateTime)
    attendance_date = db.Column(db.Date, nullable=False)
    
    # Location data (GPS from QR scan)
    check_in_latitude = db.Column(db.Float)
    check_in_longitude = db.Column(db.Float)
    check_in_accuracy = db.Column(db.Float)
    check_out_latitude = db.Column(db.Float)
    check_out_longitude = db.Column(db.Float)
    check_out_accuracy = db.Column(db.Float)
    
    # Work site and QR code
    work_site_id = db.Column(db.String(50))
    qr_code_scanned = db.Column(db.String(100))
    
    # Status and validation
    status = db.Column(db.String(20), default='Checked In')  # 'Checked In', 'Checked Out', 'Auto Checkout'
    is_valid = db.Column(db.Boolean, default=True)
    validation_message = db.Column(db.Text)
    
    # Hours worked
    hours_worked = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'status': self.status,
            'hours_worked': round(float(self.hours_worked or 0), 2),
            'work_site_id': self.work_site_id or '',
            'is_valid': bool(self.is_valid),
            'validation_message': self.validation_message or ''
        }


class QCFeedback(db.Model):
    """Quality Control video feedback"""
    __tablename__ = 'qc_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Video info
    video_id = db.Column(db.String(100))
    task_name = db.Column(db.String(200))
    video_duration = db.Column(db.Float)  # in minutes
    recorded_date = db.Column(db.Date)
    
    # QC Status
    qc_status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Rejected', 'Trimmed'
    approval_percentage = db.Column(db.Float)
    
    # Feedback categories
    wrist_camera_mismatch = db.Column(db.Boolean, default=False)
    hands_not_visible = db.Column(db.Boolean, default=False)
    poor_lighting = db.Column(db.Boolean, default=False)
    wrong_environment = db.Column(db.Boolean, default=False)
    shaky_camera = db.Column(db.Boolean, default=False)
    video_too_short = db.Column(db.Boolean, default=False)
    head_cap_not_worn = db.Column(db.Boolean, default=False)
    wrong_task_selected = db.Column(db.Boolean, default=False)
    video_not_playing = db.Column(db.Boolean, default=False)
    wrist_camera_not_worn = db.Column(db.Boolean, default=False)
    blurry_video = db.Column(db.Boolean, default=False)
    task_too_slow = db.Column(db.Boolean, default=False)
    irrelevant_video = db.Column(db.Boolean, default=False)
    pretending_working = db.Column(db.Boolean, default=False)
    rejected_on_recheck = db.Column(db.Boolean, default=False)
    
    # QC Comments
    qc_comments = db.Column(db.Text)
    qc_reviewer = db.Column(db.String(100))
    
    # Timestamps
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'video_id': self.video_id or '',
            'task_name': self.task_name or '',
            'video_duration': round(float(self.video_duration or 0), 2),
            'recorded_date': self.recorded_date.isoformat() if self.recorded_date else None,
            'qc_status': self.qc_status,
            'approval_percentage': round(float(self.approval_percentage or 0), 2),
            'issues': {
                'wrist_camera_mismatch': bool(self.wrist_camera_mismatch),
                'hands_not_visible': bool(self.hands_not_visible),
                'poor_lighting': bool(self.poor_lighting),
                'wrong_environment': bool(self.wrong_environment),
                'shaky_camera': bool(self.shaky_camera),
                'video_too_short': bool(self.video_too_short),
                'head_cap_not_worn': bool(self.head_cap_not_worn),
                'wrong_task_selected': bool(self.wrong_task_selected),
                'video_not_playing': bool(self.video_not_playing),
                'wrist_camera_not_worn': bool(self.wrist_camera_not_worn),
                'blurry_video': bool(self.blurry_video),
                'task_too_slow': bool(self.task_too_slow),
                'irrelevant_video': bool(self.irrelevant_video),
                'pretending_working': bool(self.pretending_working),
                'rejected_on_recheck': bool(self.rejected_on_recheck)
            },
            'qc_comments': self.qc_comments or '',
            'qc_reviewer': self.qc_reviewer or '',
            'submitted_date': self.submitted_date.isoformat() if self.submitted_date else None,
            'reviewed_date': self.reviewed_date.isoformat() if self.reviewed_date else None
        }


class WorkSite(db.Model):
    """Work site locations for QR scanning"""
    __tablename__ = 'work_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.String(50), unique=True, nullable=False)
    site_name = db.Column(db.String(200), nullable=False)
    
    # Location
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    allowed_radius_meters = db.Column(db.Integer, default=150)
    gps_accuracy_limit_meters = db.Column(db.Integer, default=100)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    qr_code_data = db.Column(db.String(200), unique=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'site_name': self.site_name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'allowed_radius_meters': self.allowed_radius_meters,
            'gps_accuracy_limit_meters': self.gps_accuracy_limit_meters,
            'is_active': bool(self.is_active),
            'qr_code_data': self.qr_code_data or ''
        }
