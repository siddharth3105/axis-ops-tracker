"""
Analytics and performance tracking routes
SQLite-compatible (strftime instead of date_trunc)
"""
from flask import Blueprint, render_template, jsonify
from app.models import Employee, Performance, Attendance
from app import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@bp.route('/')
def index():
    return render_template('analytics.html')


@bp.route('/api/performance/overview')
def performance_overview():
    try:
        top_quality = db.session.query(
            Employee.name,
            Employee.employee_id,
            Performance.quality_percentage,
            Performance.total_production_hours,
            Performance.total_videos
        ).join(Performance, Performance.employee_id == Employee.id
        ).order_by(desc(Performance.quality_percentage)).limit(10).all()

        top_production = db.session.query(
            Employee.name,
            Employee.employee_id,
            Performance.total_production_hours,
            Performance.quality_percentage,
            Performance.total_videos
        ).join(Performance, Performance.employee_id == Employee.id
        ).order_by(desc(Performance.total_production_hours)).limit(10).all()

        supervisor_performance = db.session.query(
            Employee.supervisor,
            func.avg(Performance.quality_percentage).label('avg_quality'),
            func.sum(Performance.total_production_hours).label('total_hours'),
            func.count(Employee.id).label('employee_count')
        ).join(Performance, Performance.employee_id == Employee.id
        ).filter(Employee.supervisor.isnot(None), Employee.supervisor != ''
        ).group_by(Employee.supervisor).all()

        return jsonify({
            'success': True,
            'top_quality': [{
                'name': r[0], 'employee_id': r[1],
                'quality': round(float(r[2] or 0), 2),
                'hours':   round(float(r[3] or 0), 2),
                'videos':  int(r[4] or 0)
            } for r in top_quality],
            'top_production': [{
                'name': r[0], 'employee_id': r[1],
                'hours':   round(float(r[2] or 0), 2),
                'quality': round(float(r[3] or 0), 2),
                'videos':  int(r[4] or 0)
            } for r in top_production],
            'supervisor_performance': [{
                'supervisor':     r[0],
                'avg_quality':    round(float(r[1] or 0), 2),
                'total_hours':    round(float(r[2] or 0), 2),
                'employee_count': int(r[3] or 0)
            } for r in supervisor_performance]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/attendance/summary')
def attendance_summary():
    try:
        thirty_days_ago = (datetime.now() - timedelta(days=30)).date()

        attendance_data = db.session.query(
            Attendance.date,
            func.count(Attendance.id).label('present_count'),
            func.sum(Attendance.hours_worked).label('total_hours')
        ).filter(
            Attendance.date >= thirty_days_ago,
            Attendance.status == 'Present'
        ).group_by(Attendance.date).order_by(Attendance.date).all()

        employee_attendance = db.session.query(
            Employee.name,
            Employee.employee_id,
            func.count(Attendance.id).label('days_present'),
            func.sum(Attendance.hours_worked).label('total_hours')
        ).join(Attendance, Attendance.employee_id == Employee.id
        ).filter(Attendance.date >= thirty_days_ago
        ).group_by(Employee.id
        ).order_by(desc(func.count(Attendance.id))).limit(20).all()

        def safe_date(d):
            return d.isoformat() if hasattr(d, 'isoformat') else str(d)

        return jsonify({
            'success': True,
            'daily_attendance': [{
                'date': safe_date(r[0]),
                'present_count': int(r[1] or 0),
                'total_hours':   round(float(r[2] or 0), 2)
            } for r in attendance_data],
            'employee_attendance': [{
                'name': r[0], 'employee_id': r[1],
                'days_present': int(r[2] or 0),
                'total_hours':  round(float(r[3] or 0), 2)
            } for r in employee_attendance]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/trends')
def trends():
    """Monthly trends — uses SQLite strftime, NOT PostgreSQL date_trunc"""
    try:
        twelve_months_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')

        employee_growth = db.session.query(
            func.strftime('%Y-%m', Employee.created_at).label('month'),
            func.count(Employee.id).label('count')
        ).filter(Employee.created_at >= twelve_months_ago
        ).group_by('month').order_by('month').all()

        quality_trend = db.session.query(
            func.strftime('%Y-%m', Performance.recorded_date).label('month'),
            func.avg(Performance.quality_percentage).label('avg_quality')
        ).filter(Performance.recorded_date >= twelve_months_ago
        ).group_by('month').order_by('month').all()

        return jsonify({
            'success': True,
            'employee_growth': [{'month': r[0], 'count': int(r[1] or 0)} for r in employee_growth],
            'quality_trend':   [{'month': r[0], 'avg_quality': round(float(r[1] or 0), 2)} for r in quality_trend]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
