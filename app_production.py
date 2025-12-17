"""Production Flask app for Vercel - Fixed version"""
from app import create_app
import os

# Set Vercel environment flag
os.environ['VERCEL'] = '1'

# Create the Flask application instance for production
try:
    app = create_app('production')
    print("✅ App created successfully")
except Exception as e:
    print(f"❌ App creation failed: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback minimal app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'error',
            'message': 'App initialization failed',
            'error': str(e)
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'error', 'details': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
