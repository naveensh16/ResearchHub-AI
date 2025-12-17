"""Diagnostic app to find the failing import"""
from flask import Flask, jsonify
import os
import sys

os.environ['VERCEL'] = '1'

app = Flask(__name__)

@app.route('/')
def index():
    results = []
    
    # Test imports one by one
    try:
        from flask_sqlalchemy import SQLAlchemy
        results.append({"module": "flask_sqlalchemy", "status": "✅ OK"})
    except Exception as e:
        results.append({"module": "flask_sqlalchemy", "status": f"❌ {str(e)}"})
    
    try:
        from flask_login import LoginManager
        results.append({"module": "flask_login", "status": "✅ OK"})
    except Exception as e:
        results.append({"module": "flask_login", "status": f"❌ {str(e)}"})
    
    try:
        from flask_socketio import SocketIO
        results.append({"module": "flask_socketio", "status": "✅ OK"})
    except Exception as e:
        results.append({"module": "flask_socketio", "status": f"❌ {str(e)}"})
    
    try:
        from flask_cors import CORS
        results.append({"module": "flask_cors", "status": "✅ OK"})
    except Exception as e:
        results.append({"module": "flask_cors", "status": f"❌ {str(e)}"})
    
    try:
        from config import config
        results.append({"module": "config", "status": "✅ OK"})
    except Exception as e:
        results.append({"module": "config", "status": f"❌ {str(e)}"})
    
    try:
        from app import create_app
        results.append({"module": "app.create_app", "status": "✅ OK"})
    except Exception as e:
        results.append({"module": "app.create_app", "status": f"❌ {str(e)}"})
        import traceback
        results.append({"traceback": traceback.format_exc()})
    
    return jsonify({
        "test": "Import Diagnostic",
        "python_version": sys.version,
        "results": results
    })

@app.route('/health')
def health():
    return jsonify({"status": "diagnostic_mode"})

if __name__ == '__main__':
    app.run(debug=True)
