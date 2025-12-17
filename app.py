"""Flask application entrypoint for Vercel deployment."""
from app import create_app
import os

# Set Vercel environment flag
os.environ['VERCEL'] = '1'

# Create the Flask application instance for production
app = create_app('production')

# This is required for Vercel
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
