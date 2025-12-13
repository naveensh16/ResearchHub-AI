"""
ResearchHub AI - Profile Routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<int:user_id>')
@login_required
def view(user_id):
    """View user profile"""
    user = User.query.get_or_404(user_id)
    return render_template('profile/view.html', user=user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit own profile"""
    if request.method == 'POST':
        current_user.name = request.form.get('name', '').strip()
        current_user.institution = request.form.get('institution', '').strip()
        current_user.bio = request.form.get('bio', '').strip()
        current_user.research_domains = request.form.get('research_domains', '').strip()
        current_user.current_interests = request.form.get('current_interests', '').strip()
        current_user.availability = request.form.get('availability', 'Solo')
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.view', user_id=current_user.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update profile.', 'danger')
            print(f"Profile update error: {e}")
    
    return render_template('profile/edit.html')

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Account settings"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
            else:
                current_user.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully!', 'success')
    
    return render_template('profile/settings.html')
