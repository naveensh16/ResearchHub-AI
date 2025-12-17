"""Minimal Flask app for Vercel - troubleshooting version"""
from flask import Flask, jsonify
import os

os.environ['VERCEL'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minimal-test-key'

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'ResearchHub AI - Minimal Version',
        'version': '1.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)
