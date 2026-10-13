"""
Payment tracking routes
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import Employee, Payment
from app import db
from sqlalchemy import func, desc
from datetime import datetime

bp = Blueprint('payments', __name__, url_prefix='/payments')


def _parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, '%Y-%m-%d').date()
    except Exception:
        return None


@bp.route('/')
def index():
    return render_template('payments.html')


@bp.route('/api/list')
def list_payments():
    try:
        status = request.args.get('status', 'all')
        query = db.session.query(Payment, Employee.name, Employee.employee_id
                                 ).join(Employee, Employee.id == Payment.employee_id)
        if status != 'all':
            query = query.filter(Payment.payment_status == status)

        rows = query.order_by(desc(Payment.created_at)).all()
        result = []
        for pay, emp_name, emp_id in rows:
            d = pay.to_dict()
            d['employee_name'] = emp_name
            d['employee_code'] = emp_id
            result.append(d)

        return jsonify({'success': True, 'payments': result, 'count': len(result)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/create', methods=['POST'])
def create_payment():
    try:
        data = request.get_json() or {}
        payment = Payment(
            employee_id       = int(data['employee_id']),
            payment_date      = _parse_date(data.get('payment_date')),
            hours_processed   = float(data.get('hours_processed') or 0),
            amount_transferred= float(data.get('amount_transferred') or 0),
            last_payment_date = _parse_date(data.get('last_payment_date')),
            payment_status    = data.get('payment_status', 'Pending')
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': 'Payment record created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/<int:payment_id>/update', methods=['PUT'])
def update_payment(payment_id):
    try:
        payment = Payment.query.get_or_404(payment_id)
        data    = request.get_json() or {}
        DATE_FIELDS = {'payment_date', 'last_payment_date'}
        SKIP_FIELDS = {'id', 'created_at', 'employee_id'}

        for key, value in data.items():
            if key in SKIP_FIELDS or not hasattr(payment, key):
                continue
            if key in DATE_FIELDS:
                setattr(payment, key, _parse_date(value))
            else:
                setattr(payment, key, value)

        db.session.commit()
        return jsonify({
            'success': True,
            'payment': payment.to_dict(),
            'message': 'Payment updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/summary')
def payment_summary():
    try:
        total_paid = db.session.query(
            func.sum(Payment.amount_transferred)
        ).filter(Payment.payment_status == 'Completed').scalar() or 0

        pending_amount = db.session.query(
            func.sum(Payment.amount_transferred)
        ).filter(Payment.payment_status == 'Pending').scalar() or 0

        status_counts = db.session.query(
            Payment.payment_status,
            func.count(Payment.id),
            func.sum(Payment.amount_transferred)
        ).group_by(Payment.payment_status).all()

        recent_rows = db.session.query(
            Payment, Employee.name, Employee.employee_id
        ).join(Employee, Employee.id == Payment.employee_id
        ).order_by(desc(Payment.created_at)).limit(10).all()

        recent = []
        for pay, emp_name, emp_id in recent_rows:
            d = pay.to_dict()
            d['employee_name'] = emp_name
            d['employee_code'] = emp_id
            recent.append(d)

        return jsonify({
            'success': True,
            'summary': {
                'total_paid':     round(float(total_paid), 2),
                'pending_amount': round(float(pending_amount), 2),
                'status_breakdown': [{
                    'status': st,
                    'count':  int(cnt or 0),
                    'total':  round(float(tot or 0), 2)
                } for st, cnt, tot in status_counts]
            },
            'recent_payments': recent
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/employee/<int:employee_id>')
def employee_payments(employee_id):
    try:
        payments = Payment.query.filter_by(employee_id=employee_id
                   ).order_by(desc(Payment.created_at)).all()
        total = sum(p.amount_transferred for p in payments)
        return jsonify({
            'success': True,
            'payments': [p.to_dict() for p in payments],
            'total': round(total, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
