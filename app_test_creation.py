"""Test actual app creation"""
from flask import Flask, jsonify
import os
import sys
import traceback

os.environ['VERCEL'] = '1'

app = Flask(__name__)

@app.route('/')
def index():
    result = {"test": "App Creation Test"}
    
    try:
        # Import works (we know this from previous test)
        from app import create_app
        result["import"] = "✅ create_app imported"
        
        # Now try to actually create the app
        test_app = create_app('production')
        result["creation"] = "✅ create_app() succeeded"
        result["app_name"] = str(test_app)
        result["routes"] = [str(rule) for rule in test_app.url_map.iter_rules()][:10]
        
    except Exception as e:
        result["creation"] = f"❌ create_app() failed: {str(e)}"
        result["error_type"] = type(e).__name__
        result["traceback"] = traceback.format_exc()
    
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "testing_app_creation"})

if __name__ == '__main__':
    app.run(debug=True)
