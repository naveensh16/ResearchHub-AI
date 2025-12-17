"""
ResearchHub AI - Flask Application Factory
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_name='development'):
    """Application factory pattern"""
    instance_path = None
    if os.environ.get('VERCEL'):
        # Vercel file system is read-only except /tmp
        instance_path = '/tmp/researchhub-instance'
    elif os.environ.get('FLASK_INSTANCE_PATH'):
        instance_path = os.environ.get('FLASK_INSTANCE_PATH')

    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
        try:
            os.makedirs(app.instance_path, exist_ok=True)
        except OSError:
            # Ignore if directory cannot be created (may already exist or be read-only)
            pass
    else:
        app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, async_mode=app.config['SOCKETIO_ASYNC_MODE'])
    CORS(app)
    
    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import auth, main, profile, research, project, chat, ai_paper, dashboard
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(research.bp)
    app.register_blueprint(project.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(ai_paper.bp)
    app.register_blueprint(dashboard.bp)
    
    # Register SocketIO events (skip in serverless)
    if not os.environ.get('VERCEL'):
        from app.sockets import chat_events
        chat_events.register_handlers(socketio)
    
    # Create database tables (skip in serverless environments)
    if not os.environ.get('VERCEL'):
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully!")
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers"""
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
