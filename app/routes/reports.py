"""
Reports generation routes
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import Employee, Performance, Payment
from app import db
from sqlalchemy import func
from datetime import datetime
import csv
import io

bp = Blueprint('reports', __name__, url_prefix='/reports')


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except Exception:
        return None


def _csv_response(rows, headers, filename):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return jsonify({
        'success': True,
        'data': output.getvalue(),
        'filename': filename
    })


@bp.route('/')
def index():
    return render_template('reports.html')


@bp.route('/api/generate/employee-roster')
def employee_roster():
    try:
        employees = Employee.query.all()
        rows = [[
            e.employee_id, e.name, e.email, e.mobile or '',
            e.shift or '', e.weekoff_day or '', e.supervisor or '',
            e.status,
            'Yes' if e.is_resident else 'No',
            e.date_of_joining.isoformat() if e.date_of_joining else '',
            e.work_site or ''
        ] for e in employees]

        return _csv_response(
            rows,
            ['Employee ID','Name','Email','Mobile','Shift','Weekoff Day',
             'Supervisor','Status','Is Resident','Date of Joining','Work Site'],
            f'employee_roster_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/generate/performance-report')
def performance_report():
    try:
        results = db.session.query(
            Employee.employee_id, Employee.name, Employee.supervisor,
            Performance.total_days_worked, Performance.total_production_hours,
            Performance.quality_percentage, Performance.total_videos
        ).join(Performance, Performance.employee_id == Employee.id).all()

        rows = [[r[0], r[1], r[2] or '',
                 int(r[3] or 0), round(float(r[4] or 0), 2),
                 round(float(r[5] or 0), 2), int(r[6] or 0)] for r in results]

        return _csv_response(
            rows,
            ['Employee ID','Name','Supervisor','Days Worked',
             'Production Hours','Quality %','Total Videos'],
            f'performance_report_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/generate/payment-report')
def payment_report():
    try:
        start_date = _parse_date(request.args.get('start_date'))
        end_date   = _parse_date(request.args.get('end_date'))

        query = db.session.query(
            Employee.employee_id, Employee.name,
            Payment.payment_date, Payment.hours_processed,
            Payment.amount_transferred, Payment.payment_status
        ).join(Employee, Employee.id == Payment.employee_id)

        if start_date:
            query = query.filter(Payment.payment_date >= start_date)
        if end_date:
            query = query.filter(Payment.payment_date <= end_date)

        results = query.all()
        rows = [[r[0], r[1],
                 r[2].isoformat() if r[2] else '',
                 round(float(r[3] or 0), 2),
                 round(float(r[4] or 0), 2),
                 r[5]] for r in results]

        return _csv_response(
            rows,
            ['Employee ID','Name','Payment Date','Hours Processed',
             'Amount Transferred (₹)','Status'],
            f'payment_report_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/generate/supervisor-report')
def supervisor_report():
    try:
        results = db.session.query(
            Employee.supervisor,
            func.count(Employee.id).label('team_size'),
            func.avg(Performance.quality_percentage).label('avg_quality'),
            func.sum(Performance.total_production_hours).label('total_hours')
        ).join(Performance, Performance.employee_id == Employee.id
        ).filter(Employee.supervisor.isnot(None), Employee.supervisor != ''
        ).group_by(Employee.supervisor).all()

        rows = [[r[0], int(r[1] or 0),
                 round(float(r[2] or 0), 2),
                 round(float(r[3] or 0), 2)] for r in results]

        return _csv_response(
            rows,
            ['Supervisor','Team Size','Avg Quality %','Total Production Hours'],
            f'supervisor_report_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
