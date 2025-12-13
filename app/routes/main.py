"""
ResearchHub AI - Main Routes
"""
from flask import Blueprint, render_template
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for('dashboard.index'))
    return render_template('main/landing.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@bp.route('/features')
def features():
    """Features page"""
    return render_template('main/features.html')
