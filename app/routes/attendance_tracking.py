"""
Attendance Tracking Routes - QR-based check-in/check-out
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import Employee, AttendanceRecord, WorkSite
from app import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, date
import math

bp = Blueprint('attendance_tracking', __name__, url_prefix='/attendance')


@bp.route('/')
def index():
    return render_template('attendance_tracking.html')


@bp.route('/api/check-in', methods=['POST'])
def check_in():
    """Process QR code check-in"""
    try:
        data = request.get_json() or {}
        employee_id = int(data.get('employee_id'))
        qr_code = data.get('qr_code')
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        accuracy = float(data.get('accuracy', 0))
        
        # Validate employee
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'success': False, 'error': 'Employee not found'}), 404
        
        if employee.status != 'Active':
            return jsonify({'success': False, 'error': 'Employee account is inactive'}), 400
        
        # Validate work site from QR code
        work_site = WorkSite.query.filter_by(qr_code_data=qr_code, is_active=True).first()
        if not work_site:
            return jsonify({'success': False, 'error': 'QR code is not registered or inactive'}), 400
        
        # Check GPS accuracy
        if accuracy > work_site.gps_accuracy_limit_meters:
            return jsonify({
                'success': False,
                'error': f'GPS accuracy too low ({accuracy}m). Required: {work_site.gps_accuracy_limit_meters}m. Move to open area.'
            }), 400
        
        # Check if within allowed radius
        distance = calculate_distance(latitude, longitude, work_site.latitude, work_site.longitude)
        if distance > work_site.allowed_radius_meters:
            return jsonify({
                'success': False,
                'error': f'You are {distance}m from work site. Allowed: {work_site.allowed_radius_meters}m'
            }), 400
        
        # Check for existing attendance today
        today = date.today()
        existing = AttendanceRecord.query.filter_by(
            employee_id=employee_id,
            attendance_date=today
        ).first()
        
        if existing:
            # If resident or already checked in, don't allow duplicate
            if employee.is_resident:
                return jsonify({'success': False, 'error': 'Attendance already recorded for today'}), 400
            
            if existing.status == 'Checked In':
                # Check if 5 minutes have passed (prevent accidental checkout)
                time_diff = (datetime.now() - existing.check_in_time).total_seconds() / 60
                if time_diff < 5:
                    return jsonify({
                        'success': False,
                        'error': 'You have just checked in. Scan again when leaving to check out.'
                    }), 400
                
                # This is a checkout
                return process_checkout(existing, latitude, longitude, accuracy)
            else:
                return jsonify({'success': False, 'error': 'Your check-in and check-out are already recorded for today'}), 400
        
        # Create new check-in record
        attendance = AttendanceRecord(
            employee_id=employee_id,
            attendance_date=today,
            check_in_time=datetime.now(),
            check_in_latitude=latitude,
            check_in_longitude=longitude,
            check_in_accuracy=accuracy,
            work_site_id=work_site.site_id,
            qr_code_scanned=qr_code,
            status='Checked In',
            is_valid=True
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Attendance Recorded',
            'attendance': attendance.to_dict(),
            'check_in_time': attendance.check_in_time.strftime('%H:%M')
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


def process_checkout(attendance, latitude, longitude, accuracy):
    """Process checkout for existing check-in"""
    try:
        checkout_time = datetime.now()
        hours_worked = (checkout_time - attendance.check_in_time).total_seconds() / 3600
        
        # Update attendance record
        attendance.check_out_time = checkout_time
        attendance.check_out_latitude = latitude
        attendance.check_out_longitude = longitude
        attendance.check_out_accuracy = accuracy
        attendance.hours_worked = hours_worked
        attendance.status = 'Checked Out'
        attendance.updated_at = checkout_time
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Checked Out Successfully',
            'attendance': attendance.to_dict(),
            'hours_worked': round(hours_worked, 2)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/today-status/<int:employee_id>')
def today_status(employee_id):
    """Get today's attendance status for an employee"""
    try:
        today = date.today()
        attendance = AttendanceRecord.query.filter_by(
            employee_id=employee_id,
            attendance_date=today
        ).first()
        
        if attendance:
            return jsonify({
                'success': True,
                'has_attendance': True,
                'attendance': attendance.to_dict()
            })
        else:
            return jsonify({
                'success': True,
                'has_attendance': False,
                'message': 'Attendance not yet recorded for today'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/list')
def list_attendance():
    """List attendance records with filters"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        employee_id = request.args.get('employee_id')
        status = request.args.get('status', 'all')
        
        query = db.session.query(
            AttendanceRecord,
            Employee.name,
            Employee.employee_id.label('emp_code')
        ).join(Employee, Employee.id == AttendanceRecord.employee_id)
        
        if start_date:
            query = query.filter(AttendanceRecord.attendance_date >= start_date)
        if end_date:
            query = query.filter(AttendanceRecord.attendance_date <= end_date)
        if employee_id:
            query = query.filter(AttendanceRecord.employee_id == int(employee_id))
        if status != 'all':
            query = query.filter(AttendanceRecord.status == status)
        
        records = query.order_by(desc(AttendanceRecord.attendance_date), desc(AttendanceRecord.check_in_time)).all()
        
        result = []
        for att, emp_name, emp_code in records:
            d = att.to_dict()
            d['employee_name'] = emp_name
            d['employee_code'] = emp_code
            result.append(d)
        
        return jsonify({'success': True, 'records': result, 'count': len(result)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/summary')
def attendance_summary():
    """Get attendance summary stats"""
    try:
        today = date.today()
        
        # Today's stats
        today_checked_in = AttendanceRecord.query.filter(
            AttendanceRecord.attendance_date == today,
            AttendanceRecord.status.in_(['Checked In', 'Checked Out'])
        ).count()
        
        today_checked_out = AttendanceRecord.query.filter(
            AttendanceRecord.attendance_date == today,
            AttendanceRecord.status == 'Checked Out'
        ).count()
        
        # Week stats
        week_ago = today - timedelta(days=7)
        week_attendance = db.session.query(
            AttendanceRecord.attendance_date,
            func.count(AttendanceRecord.id).label('count')
        ).filter(
            AttendanceRecord.attendance_date >= week_ago
        ).group_by(AttendanceRecord.attendance_date).all()
        
        # Top employees by attendance
        top_employees = db.session.query(
            Employee.name,
            Employee.employee_id,
            func.count(AttendanceRecord.id).label('days_present')
        ).join(AttendanceRecord, AttendanceRecord.employee_id == Employee.id
        ).filter(AttendanceRecord.attendance_date >= week_ago
        ).group_by(Employee.id
        ).order_by(desc('days_present')).limit(10).all()
        
        return jsonify({
            'success': True,
            'summary': {
                'today_checked_in': today_checked_in,
                'today_checked_out': today_checked_out,
                'today_still_working': today_checked_in - today_checked_out,
                'week_attendance': [{'date': str(d), 'count': c} for d, c in week_attendance],
                'top_employees': [{'name': n, 'employee_id': e, 'days': d} for n, e, d in top_employees]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/work-sites')
def list_work_sites():
    """List all active work sites"""
    try:
        sites = WorkSite.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'work_sites': [s.to_dict() for s in sites]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in meters"""
    R = 6371000  # Earth's radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return round(distance)
