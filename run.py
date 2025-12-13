"""
ResearchHub AI - Application Entry Point
"""
from app import create_app, socketio
import os

# Get environment
env = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(env)

if __name__ == '__main__':
    # Create upload folder if not exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run with SocketIO
    print("\n" + "="*60)
    print("🚀 ResearchHub AI - Starting...")
    print("="*60)
    print(f"📌 Environment: {env}")
    print(f"🔧 Debug Mode: {app.config['DEBUG']}")
    print(f"🤖 AI Provider: {app.config['LLM_PROVIDER']}")
    print(f"💾 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("="*60 + "\n")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG'],
        allow_unsafe_werkzeug=True
    )
