"""Flask app for Vercel - Step 2: Add app factory without database"""
from flask import Flask, jsonify, render_template_string
import os

os.environ['VERCEL'] = '1'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-12345')
    
    @app.route('/')
    def index():
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>ResearchHub AI</title></head>
        <body>
            <h1>ResearchHub AI</h1>
            <p>Successfully deployed to Vercel!</p>
            <ul>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/debug">Debug Info</a></li>
            </ul>
        </body>
        </html>
        """
        return render_template_string(html)
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'stage': 'step2-factory'})
    
    @app.route('/debug')
    def debug():
        return jsonify({
            'routes': [str(rule) for rule in app.url_map.iter_rules()],
            'config': {
                'SECRET_KEY': 'configured' if app.config['SECRET_KEY'] else 'missing',
                'VERCEL': os.environ.get('VERCEL')
            }
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
