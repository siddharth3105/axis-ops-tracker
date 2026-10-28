"""
Axis Ops Tracker - Flask Application
Main application initialization
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'axis-ops-tracker-secret-key-change-in-production'

    # Store DB in the /data folder beside the app package
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, 'data', 'axis_ops.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes import main, employees, analytics, payments, reports, attendance_tracking, qc_feedback, followup
    from app.routes.ai_call import bp as ai_call_bp
    app.register_blueprint(main.bp)
    app.register_blueprint(employees.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(attendance_tracking.bp)
    app.register_blueprint(qc_feedback.bp)
    app.register_blueprint(followup.bp)
    app.register_blueprint(ai_call_bp)

    # Google Sheets sync endpoint
    @app.route('/api/sync/sheets', methods=['POST'])
    def sync_sheets():
        try:
            from app.utils.google_sheets import GoogleSheetsSync
            
            sync = GoogleSheetsSync()
            result = sync.sync_all()
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Data synced successfully to Google Sheets',
                    'synced': result['synced'],
                    'spreadsheet_url': GoogleSheetsSync.SPREADSHEET_URL
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Sync failed'),
                    'synced': result.get('synced', []),
                    'errors': result.get('errors', [])
                }), 500
                
        except FileNotFoundError as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'setup_required': True,
                'instructions': 'See GOOGLE_SHEETS_SETUP.md for setup instructions'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Sync error: {str(e)}'
            }), 500

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
