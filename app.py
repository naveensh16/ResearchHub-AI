"""Flask application entrypoint for Vercel deployment."""
from app import create_app
import os

# Set Vercel environment flag
os.environ['VERCEL'] = '1'

# Create the Flask application instance for production
app = create_app('production')

# Add debug endpoint
@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'ok',
        'environment': 'vercel',
        'python': os.sys.version
    }

@app.route('/debug')
def debug():
    """Debug endpoint to test app initialization"""
    import sys
    return {
        'status': 'running',
        'python_version': sys.version,
        'flask_app': str(app),
        'blueprints': list(app.blueprints.keys()),
        'routes': [str(rule) for rule in app.url_map.iter_rules()]
    }

# This is required for Vercel
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
