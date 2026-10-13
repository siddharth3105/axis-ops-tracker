"""
Employee management routes
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import Employee, Performance, Payment, Attendance
from app import db
from datetime import datetime

bp = Blueprint('employees', __name__, url_prefix='/employees')


@bp.route('/')
def index():
    return render_template('employees.html')


@bp.route('/api/list')
def list_employees():
    try:
        status     = request.args.get('status', 'all')
        supervisor = request.args.get('supervisor', 'all')
        shift      = request.args.get('shift', 'all')
        search     = request.args.get('search', '').strip()

        query = Employee.query
        if status != 'all':
            query = query.filter_by(status=status)
        if supervisor != 'all':
            query = query.filter_by(supervisor=supervisor)
        if shift != 'all':
            query = query.filter_by(shift=shift)
        if search:
            like = f'%{search}%'
            query = query.filter(
                (Employee.name.ilike(like)) |
                (Employee.employee_id.ilike(like)) |
                (Employee.email.ilike(like))
            )

        employees = query.all()
        return jsonify({
            'success': True,
            'employees': [e.to_dict() for e in employees],
            'count': len(employees)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/<int:employee_id>')
def get_employee(employee_id):
    try:
        employee    = Employee.query.get_or_404(employee_id)
        performance = Performance.query.filter_by(employee_id=employee_id).first()
        payments    = Payment.query.filter_by(employee_id=employee_id).all()
        attendance  = Attendance.query.filter_by(
            employee_id=employee_id
        ).order_by(Attendance.date.desc()).limit(30).all()

        return jsonify({
            'success': True,
            'employee':    employee.to_dict(),
            'performance': performance.to_dict() if performance else None,
            'payments':    [p.to_dict() for p in payments],
            'attendance':  [a.to_dict() for a in attendance]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except Exception:
        return None


@bp.route('/api/create', methods=['POST'])
def create_employee():
    try:
        data = request.get_json() or {}

        if Employee.query.filter_by(employee_id=data.get('employee_id', '')).first():
            return jsonify({'success': False, 'error': 'Employee ID already exists'}), 400

        employee = Employee(
            employee_id       = data['employee_id'],
            name              = data['name'],
            email             = data['email'],
            mobile            = data.get('mobile'),
            shift             = data.get('shift'),
            weekoff_day       = data.get('weekoff_day'),
            supervisor        = data.get('supervisor'),
            status            = data.get('status', 'Active'),
            is_resident       = bool(data.get('is_resident', False)),
            is_supervisor     = bool(data.get('is_supervisor', False)),
            supervisor_email  = data.get('supervisor_email'),
            work_site         = data.get('work_site'),
            date_of_joining   = _parse_date(data.get('date_of_joining')),
            user_id           = data.get('user_id'),
            accommodation        = data.get('accommodation'),
            accommodation_status = data.get('accommodation_status'),
            training_date        = _parse_date(data.get('training_date'))
        )
        db.session.add(employee)
        db.session.flush()   # get employee.id before commit

        perf = Performance(employee_id=employee.id)
        db.session.add(perf)
        db.session.commit()

        return jsonify({
            'success': True,
            'employee': employee.to_dict(),
            'message': 'Employee created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/<int:employee_id>/update', methods=['PUT'])
def update_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        data = request.get_json() or {}

        DATE_FIELDS = {'date_of_joining', 'training_date'}
        SKIP_FIELDS = {'id', 'created_at'}

        for key, value in data.items():
            if key in SKIP_FIELDS or not hasattr(employee, key):
                continue
            if key in DATE_FIELDS:
                setattr(employee, key, _parse_date(value))
            else:
                setattr(employee, key, value)

        db.session.commit()
        return jsonify({
            'success': True,
            'employee': employee.to_dict(),
            'message': 'Employee updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/<int:employee_id>/delete', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = Employee.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Employee deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/filters')
def get_filters():
    try:
        supervisors = db.session.query(Employee.supervisor).filter(
            Employee.supervisor.isnot(None),
            Employee.supervisor != ''
        ).distinct().all()

        shifts = db.session.query(Employee.shift).filter(
            Employee.shift.isnot(None),
            Employee.shift != ''
        ).distinct().all()

        return jsonify({
            'success': True,
            'supervisors': [s[0] for s in supervisors],
            'shifts':      [s[0] for s in shifts]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
