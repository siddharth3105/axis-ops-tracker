"""
QC Feedback Routes - Video quality control system
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import Employee, QCFeedback
from app import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta, date

bp = Blueprint('qc_feedback', __name__, url_prefix='/qc')


@bp.route('/')
def index():
    return render_template('qc_feedback.html')


@bp.route('/api/submit', methods=['POST'])
def submit_feedback():
    """Submit QC feedback for a video"""
    try:
        data = request.get_json() or {}
        
        feedback = QCFeedback(
            employee_id=int(data['employee_id']),
            video_id=data.get('video_id'),
            task_name=data.get('task_name'),
            video_duration=float(data.get('video_duration', 0)),
            recorded_date=_parse_date(data.get('recorded_date')),
            qc_status=data.get('qc_status', 'Pending'),
            approval_percentage=float(data.get('approval_percentage', 0)),
            
            # Issues
            wrist_camera_mismatch=bool(data.get('wrist_camera_mismatch', False)),
            hands_not_visible=bool(data.get('hands_not_visible', False)),
            poor_lighting=bool(data.get('poor_lighting', False)),
            wrong_environment=bool(data.get('wrong_environment', False)),
            shaky_camera=bool(data.get('shaky_camera', False)),
            video_too_short=bool(data.get('video_too_short', False)),
            head_cap_not_worn=bool(data.get('head_cap_not_worn', False)),
            wrong_task_selected=bool(data.get('wrong_task_selected', False)),
            video_not_playing=bool(data.get('video_not_playing', False)),
            wrist_camera_not_worn=bool(data.get('wrist_camera_not_worn', False)),
            blurry_video=bool(data.get('blurry_video', False)),
            task_too_slow=bool(data.get('task_too_slow', False)),
            irrelevant_video=bool(data.get('irrelevant_video', False)),
            pretending_working=bool(data.get('pretending_working', False)),
            rejected_on_recheck=bool(data.get('rejected_on_recheck', False)),
            
            qc_comments=data.get('qc_comments'),
            qc_reviewer=data.get('qc_reviewer'),
            reviewed_date=datetime.now() if data.get('qc_status') != 'Pending' else None
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'QC feedback submitted successfully',
            'feedback': feedback.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/list')
def list_feedback():
    """List QC feedback records"""
    try:
        status = request.args.get('status', 'all')
        employee_id = request.args.get('employee_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = db.session.query(
            QCFeedback,
            Employee.name,
            Employee.employee_id.label('emp_code')
        ).join(Employee, Employee.id == QCFeedback.employee_id)
        
        if status != 'all':
            query = query.filter(QCFeedback.qc_status == status)
        if employee_id:
            query = query.filter(QCFeedback.employee_id == int(employee_id))
        if start_date:
            query = query.filter(QCFeedback.recorded_date >= start_date)
        if end_date:
            query = query.filter(QCFeedback.recorded_date <= end_date)
        
        records = query.order_by(desc(QCFeedback.submitted_date)).all()
        
        result = []
        for qc, emp_name, emp_code in records:
            d = qc.to_dict()
            d['employee_name'] = emp_name
            d['employee_code'] = emp_code
            result.append(d)
        
        return jsonify({'success': True, 'feedback': result, 'count': len(result)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/<int:feedback_id>')
def get_feedback(feedback_id):
    """Get specific QC feedback"""
    try:
        feedback = QCFeedback.query.get_or_404(feedback_id)
        employee = Employee.query.get(feedback.employee_id)
        
        result = feedback.to_dict()
        result['employee_name'] = employee.name
        result['employee_code'] = employee.employee_id
        
        return jsonify({'success': True, 'feedback': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/<int:feedback_id>/update', methods=['PUT'])
def update_feedback(feedback_id):
    """Update QC feedback"""
    try:
        feedback = QCFeedback.query.get_or_404(feedback_id)
        data = request.get_json() or {}
        
        # Update status
        if 'qc_status' in data:
            feedback.qc_status = data['qc_status']
            if data['qc_status'] != 'Pending' and not feedback.reviewed_date:
                feedback.reviewed_date = datetime.now()
        
        # Update approval percentage
        if 'approval_percentage' in data:
            feedback.approval_percentage = float(data['approval_percentage'])
        
        # Update issues
        issue_fields = [
            'wrist_camera_mismatch', 'hands_not_visible', 'poor_lighting',
            'wrong_environment', 'shaky_camera', 'video_too_short',
            'head_cap_not_worn', 'wrong_task_selected', 'video_not_playing',
            'wrist_camera_not_worn', 'blurry_video', 'task_too_slow',
            'irrelevant_video', 'pretending_working', 'rejected_on_recheck'
        ]
        
        for field in issue_fields:
            if field in data:
                setattr(feedback, field, bool(data[field]))
        
        # Update comments and reviewer
        if 'qc_comments' in data:
            feedback.qc_comments = data['qc_comments']
        if 'qc_reviewer' in data:
            feedback.qc_reviewer = data['qc_reviewer']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'QC feedback updated successfully',
            'feedback': feedback.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/summary')
def qc_summary():
    """Get QC summary statistics"""
    try:
        # Status breakdown
        status_counts = db.session.query(
            QCFeedback.qc_status,
            func.count(QCFeedback.id).label('count'),
            func.avg(QCFeedback.approval_percentage).label('avg_approval')
        ).group_by(QCFeedback.qc_status).all()
        
        # Common issues
        issue_counts = {
            'wrist_camera_mismatch': QCFeedback.query.filter_by(wrist_camera_mismatch=True).count(),
            'hands_not_visible': QCFeedback.query.filter_by(hands_not_visible=True).count(),
            'poor_lighting': QCFeedback.query.filter_by(poor_lighting=True).count(),
            'wrong_environment': QCFeedback.query.filter_by(wrong_environment=True).count(),
            'shaky_camera': QCFeedback.query.filter_by(shaky_camera=True).count(),
            'video_too_short': QCFeedback.query.filter_by(video_too_short=True).count(),
            'blurry_video': QCFeedback.query.filter_by(blurry_video=True).count(),
            'task_too_slow': QCFeedback.query.filter_by(task_too_slow=True).count(),
            'irrelevant_video': QCFeedback.query.filter_by(irrelevant_video=True).count(),
            'pretending_working': QCFeedback.query.filter_by(pretending_working=True).count()
        }
        
        # Top issues (sorted)
        top_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Employee performance
        employee_stats = db.session.query(
            Employee.name,
            Employee.employee_id,
            func.count(QCFeedback.id).label('total_videos'),
            func.sum(func.cast(QCFeedback.qc_status == 'Approved', db.Integer)).label('approved'),
            func.avg(QCFeedback.approval_percentage).label('avg_approval')
        ).join(QCFeedback, QCFeedback.employee_id == Employee.id
        ).group_by(Employee.id
        ).order_by(desc('avg_approval')).limit(10).all()
        
        # Recent feedback
        recent = db.session.query(
            QCFeedback, Employee.name, Employee.employee_id
        ).join(Employee, Employee.id == QCFeedback.employee_id
        ).order_by(desc(QCFeedback.submitted_date)).limit(10).all()
        
        recent_feedback = []
        for qc, emp_name, emp_code in recent:
            d = qc.to_dict()
            d['employee_name'] = emp_name
            d['employee_code'] = emp_code
            recent_feedback.append(d)
        
        return jsonify({
            'success': True,
            'summary': {
                'status_breakdown': [{
                    'status': st,
                    'count': int(cnt),
                    'avg_approval': round(float(avg or 0), 2)
                } for st, cnt, avg in status_counts],
                'top_issues': [{'issue': name, 'count': count} for name, count in top_issues],
                'employee_performance': [{
                    'name': n,
                    'employee_id': e,
                    'total_videos': int(t),
                    'approved': int(a or 0),
                    'approval_rate': round(float(avg or 0), 2)
                } for n, e, t, a, avg in employee_stats],
                'recent_feedback': recent_feedback
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/employee/<int:employee_id>/stats')
def employee_qc_stats(employee_id):
    """Get QC stats for specific employee"""
    try:
        employee = Employee.query.get_or_404(employee_id)
        
        total = QCFeedback.query.filter_by(employee_id=employee_id).count()
        approved = QCFeedback.query.filter_by(employee_id=employee_id, qc_status='Approved').count()
        rejected = QCFeedback.query.filter_by(employee_id=employee_id, qc_status='Rejected').count()
        pending = QCFeedback.query.filter_by(employee_id=employee_id, qc_status='Pending').count()
        
        avg_approval = db.session.query(
            func.avg(QCFeedback.approval_percentage)
        ).filter(QCFeedback.employee_id == employee_id).scalar() or 0
        
        # Recent feedback
        recent = QCFeedback.query.filter_by(employee_id=employee_id
                ).order_by(desc(QCFeedback.submitted_date)).limit(10).all()
        
        return jsonify({
            'success': True,
            'employee': {
                'name': employee.name,
                'employee_id': employee.employee_id
            },
            'stats': {
                'total_videos': total,
                'approved': approved,
                'rejected': rejected,
                'pending': pending,
                'approval_rate': round((approved / total * 100) if total > 0 else 0, 2),
                'avg_approval_percentage': round(float(avg_approval), 2)
            },
            'recent_feedback': [f.to_dict() for f in recent]
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
