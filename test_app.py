"""Minimal test app to debug Vercel deployment"""
import os
os.environ['VERCEL'] = '1'

try:
    from flask import Flask
    print("✓ Flask imported")
    
    from flask_sqlalchemy import SQLAlchemy
    print("✓ SQLAlchemy imported")
    
    from flask_login import LoginManager
    print("✓ LoginManager imported")
    
    from flask_socketio import SocketIO
    print("✓ SocketIO imported")
    
    from flask_cors import CORS
    print("✓ CORS imported")
    
    from config import config
    print("✓ Config imported")
    
    from app import create_app
    print("✓ create_app imported")
    
    app = create_app('production')
    print("✓ App created successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
