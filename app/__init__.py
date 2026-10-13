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
    from app.routes import main, employees, analytics, payments, reports
    app.register_blueprint(main.bp)
    app.register_blueprint(employees.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(reports.bp)

    # Sync stub so the "Sync with Sheets" button in the UI doesn't 404
    @app.route('/api/sync/sheets', methods=['POST'])
    def sync_sheets_stub():
        return jsonify({
            'success': False,
            'error': (
                'Google Sheets sync requires credentials.json. '
                'See SETUP_GUIDE.md Section 2 to configure it.'
            )
        }), 501

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
