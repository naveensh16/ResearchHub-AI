"""
ResearchHub AI - Dashboard Routes
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User, Project, Message, Paper
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    """Main dashboard"""
    # Update last seen
    current_user.last_seen = datetime.utcnow()
    
    # Get active projects
    active_projects = current_user.projects.filter_by(status='Active').limit(5).all()
    
    # Get suggested researchers (matching algorithm)
    suggested = get_suggested_researchers(current_user)
    
    # Get recent unread messages count
    unread_count = Message.query.filter(
        and_(
            Message.recipient_id == current_user.id,
            Message.is_read == False
        )
    ).count()
    
    # Get recent papers
    recent_papers = current_user.papers.order_by(Paper.updated_at.desc()).limit(3).all()
    
    # Get AI alerts (papers needing review)
    papers_needing_review = current_user.papers.filter(
        or_(
            Paper.last_reviewed == None,
            Paper.last_reviewed < datetime.utcnow() - timedelta(days=7)
        )
    ).count()
    
    return render_template('dashboard/index.html',
                         active_projects=active_projects,
                         suggested_researchers=suggested[:5],
                         unread_messages=unread_count,
                         recent_papers=recent_papers,
                         papers_needing_review=papers_needing_review)

def get_suggested_researchers(user, limit=10):
    """Find researchers with matching interests"""
    if not user.research_domains:
        return []
    
    user_tags = set(user.get_domains_list())
    
    # Find users with common tags
    all_users = User.query.filter(
        User.id != user.id,
        User.is_active == True,
        User.research_domains != None
    ).all()
    
    matches = []
    for other_user in all_users:
        other_tags = set(other_user.get_domains_list())
        common = user_tags & other_tags
        
        if len(common) >= 1:  # MIN_COMMON_TAGS from config
            matches.append({
                'user': other_user,
                'common_tags': list(common),
                'score': len(common)
            })
    
    # Sort by match score
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:limit]

@bp.route('/stats')
@login_required
def stats():
    """User statistics"""
    total_projects = current_user.projects.count()
    total_papers = current_user.papers.count()
    
    return render_template('dashboard/stats.html',
                         total_projects=total_projects,
                         total_papers=total_papers)
