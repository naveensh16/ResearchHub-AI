"""
ResearchHub AI - Research Discovery & Matching Routes
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, collaboration_requests
from sqlalchemy import or_, and_

bp = Blueprint('research', __name__, url_prefix='/research')

@bp.route('/discover')
@login_required
def discover():
    """Discover researchers"""
    search_query = request.args.get('q', '').strip()
    domain_filter = request.args.get('domain', '').strip()
    
    query = User.query.filter(
        User.id != current_user.id,
        User.is_active == True
    )
    
    if search_query:
        query = query.filter(
            or_(
                User.name.ilike(f'%{search_query}%'),
                User.institution.ilike(f'%{search_query}%'),
                User.research_domains.ilike(f'%{search_query}%'),
                User.current_interests.ilike(f'%{search_query}%')
            )
        )
    
    if domain_filter:
        query = query.filter(User.research_domains.ilike(f'%{domain_filter}%'))
    
    researchers = query.all()
    
    # Calculate match scores
    user_tags = set(current_user.get_domains_list()) if current_user.research_domains else set()
    
    researcher_data = []
    for researcher in researchers:
        researcher_tags = set(researcher.get_domains_list()) if researcher.research_domains else set()
        common_tags = user_tags & researcher_tags
        
        researcher_data.append({
            'user': researcher,
            'common_tags': list(common_tags),
            'match_score': len(common_tags)
        })
    
    # Sort by match score
    researcher_data.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render_template('research/discover.html',
                         researchers=researcher_data,
                         search_query=search_query,
                         domain_filter=domain_filter)

@bp.route('/suggestions')
@login_required
def suggestions():
    """Get collaboration suggestions"""
    from app.routes.dashboard import get_suggested_researchers
    
    suggested = get_suggested_researchers(current_user, limit=20)
    return render_template('research/suggestions.html', suggestions=suggested)

@bp.route('/request/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    """Send collaboration request"""
    receiver = User.query.get_or_404(user_id)
    
    if receiver.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot send request to yourself'}), 400
    
    message = request.form.get('message', '').strip()
    
    # Check if request already exists
    existing = db.session.execute(
        db.select(collaboration_requests).where(
            and_(
                collaboration_requests.c.sender_id == current_user.id,
                collaboration_requests.c.receiver_id == user_id
            )
        )
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Request already sent'}), 400
    
    # Insert collaboration request
    stmt = collaboration_requests.insert().values(
        sender_id=current_user.id,
        receiver_id=user_id,
        message=message,
        status='pending'
    )
    
    try:
        db.session.execute(stmt)
        db.session.commit()
        flash(f'Collaboration request sent to {receiver.name}!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Request error: {e}")
        return jsonify({'success': False, 'message': 'Failed to send request'}), 500

@bp.route('/requests')
@login_required
def requests_page():
    """View collaboration requests"""
    # Received requests
    received = db.session.execute(
        db.select(
            collaboration_requests.c.sender_id,
            collaboration_requests.c.message,
            collaboration_requests.c.status,
            collaboration_requests.c.created_at
        ).where(
            collaboration_requests.c.receiver_id == current_user.id
        ).order_by(collaboration_requests.c.created_at.desc())
    ).all()
    
    received_data = []
    for req in received:
        sender = User.query.get(req.sender_id)
        received_data.append({
            'sender': sender,
            'message': req.message,
            'status': req.status,
            'created_at': req.created_at
        })
    
    # Sent requests
    sent = db.session.execute(
        db.select(
            collaboration_requests.c.receiver_id,
            collaboration_requests.c.message,
            collaboration_requests.c.status,
            collaboration_requests.c.created_at
        ).where(
            collaboration_requests.c.sender_id == current_user.id
        ).order_by(collaboration_requests.c.created_at.desc())
    ).all()
    
    sent_data = []
    for req in sent:
        receiver = User.query.get(req.receiver_id)
        sent_data.append({
            'receiver': receiver,
            'message': req.message,
            'status': req.status,
            'created_at': req.created_at
        })
    
    return render_template('research/requests.html',
                         received_requests=received_data,
                         sent_requests=sent_data)

@bp.route('/request/<int:sender_id>/respond', methods=['POST'])
@login_required
def respond_request(sender_id):
    """Respond to collaboration request"""
    action = request.form.get('action')  # accept or reject
    
    if action not in ['accepted', 'rejected']:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    
    # Update request status
    stmt = collaboration_requests.update().where(
        and_(
            collaboration_requests.c.sender_id == sender_id,
            collaboration_requests.c.receiver_id == current_user.id
        )
    ).values(status=action)
    
    try:
        db.session.execute(stmt)
        db.session.commit()
        flash(f'Request {action}!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Response error: {e}")
        return jsonify({'success': False, 'message': 'Failed to respond'}), 500
