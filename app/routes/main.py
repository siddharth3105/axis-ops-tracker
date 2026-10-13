"""
Main routes - Dashboard and home page
"""
from flask import Blueprint, render_template, jsonify
from app.models import Employee, Performance, Payment
from app import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('dashboard.html')


@bp.route('/api/dashboard/stats')
def dashboard_stats():
    try:
        total_employees   = Employee.query.count()
        active_employees  = Employee.query.filter_by(status='Active').count()
        inactive_employees = total_employees - active_employees
        total_supervisors = Employee.query.filter_by(is_supervisor=True).count()
        residents         = Employee.query.filter_by(is_resident=True).count()
        non_residents     = total_employees - residents

        shifts = db.session.query(
            Employee.shift, func.count(Employee.id)
        ).group_by(Employee.shift).all()
        shift_data = {s: c for s, c in shifts if s}

        supervisors = db.session.query(
            Employee.supervisor, func.count(Employee.id)
        ).filter(Employee.supervisor.isnot(None),
                 Employee.supervisor != ''
        ).group_by(Employee.supervisor).all()
        supervisor_data = {s: c for s, c in supervisors}

        total_production_hours = db.session.query(
            func.sum(Performance.total_production_hours)).scalar() or 0
        avg_quality = db.session.query(
            func.avg(Performance.quality_percentage)).scalar() or 0
        total_videos = db.session.query(
            func.sum(Performance.total_videos)).scalar() or 0
        total_payments = db.session.query(
            func.sum(Payment.amount_transferred)).scalar() or 0
        pending_payments = Payment.query.filter_by(payment_status='Pending').count()

        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_hires = Employee.query.filter(
            Employee.created_at >= seven_days_ago).count()

        return jsonify({
            'success': True,
            'stats': {
                'employees': {
                    'total': total_employees,
                    'active': active_employees,
                    'inactive': inactive_employees,
                    'recent_hires': recent_hires
                },
                'hierarchy': {
                    'supervisors': total_supervisors,
                    'supervisor_distribution': supervisor_data
                },
                'accommodation': {
                    'residents': residents,
                    'non_residents': non_residents
                },
                'shifts': shift_data,
                'performance': {
                    'total_production_hours': round(float(total_production_hours), 2),
                    'avg_quality':            round(float(avg_quality), 2),
                    'total_videos':           int(total_videos or 0)
                },
                'payments': {
                    'total_paid':    round(float(total_payments), 2),
                    'pending_count': pending_payments
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/dashboard/recent-activity')
def recent_activity():
    try:
        recent_employees = Employee.query.order_by(
            desc(Employee.created_at)).limit(5).all()
        recent_payments = Payment.query.order_by(
            desc(Payment.created_at)).limit(5).all()

        return jsonify({
            'success': True,
            'recent_employees': [e.to_dict() for e in recent_employees],
            'recent_payments':  [p.to_dict() for p in recent_payments]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
