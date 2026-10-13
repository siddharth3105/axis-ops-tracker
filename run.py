"""
Axis Ops Tracker - Main Application Entry Point
Run this file to start the Flask development server
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AXIS OPS TRACKER - Starting Server")
    print("="*60)
    print("\n📊 Dashboard will be available at: http://localhost:5000")
    print("📝 Press CTRL+C to stop the server\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
