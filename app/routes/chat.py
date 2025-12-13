"""
ResearchHub AI - Chat Routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Message, User, Project
from datetime import datetime
from sqlalchemy import or_, and_

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
@login_required
def index():
    """Chat inbox"""
    # Get recent conversations
    # 1-to-1 chats
    sent_messages = db.session.query(Message.recipient_id).filter(
        Message.sender_id == current_user.id,
        Message.recipient_id != None
    ).distinct().all()
    
    received_messages = db.session.query(Message.sender_id).filter(
        Message.recipient_id == current_user.id
    ).distinct().all()
    
    conversation_user_ids = set()
    for msg in sent_messages:
        conversation_user_ids.add(msg[0])
    for msg in received_messages:
        conversation_user_ids.add(msg[0])
    
    conversations = []
    for user_id in conversation_user_ids:
        user = User.query.get(user_id)
        if user:
            # Get last message
            last_msg = Message.query.filter(
                or_(
                    and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
                    and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
                )
            ).order_by(Message.created_at.desc()).first()
            
            # Count unread
            unread = Message.query.filter(
                Message.sender_id == user_id,
                Message.recipient_id == current_user.id,
                Message.is_read == False
            ).count()
            
            conversations.append({
                'user': user,
                'last_message': last_msg,
                'unread_count': unread
            })
    
    # Sort by last message time
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else datetime.min, reverse=True)
    
    # Get project chats
    user_projects = current_user.projects.all()
    
    return render_template('chat/index.html',
                         conversations=conversations,
                         projects=user_projects)

@bp.route('/user/<int:user_id>')
@login_required
def chat_with_user(user_id):
    """1-to-1 chat with user"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return "Cannot chat with yourself", 400
    
    # Get message history
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    # Mark messages as read
    Message.query.filter(
        Message.sender_id == user_id,
        Message.recipient_id == current_user.id,
        Message.is_read == False
    ).update({'is_read': True})
    db.session.commit()
    
    return render_template('chat/user_chat.html',
                         chat_user=user,
                         messages=messages)

@bp.route('/project/<int:project_id>')
@login_required
def project_chat(project_id):
    """Project group chat"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user is member
    is_member = project.members.filter_by(id=current_user.id).first() is not None
    
    if not is_member:
        return "Access denied", 403
    
    # Get message history
    messages = project.messages.order_by(Message.created_at.asc()).all()
    
    return render_template('chat/project_chat.html',
                         project=project,
                         messages=messages)

@bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """Send message (AJAX endpoint)"""
    data = request.get_json()
    
    content = data.get('content', '').strip()
    recipient_id = data.get('recipient_id')
    project_id = data.get('project_id')
    
    if not content:
        return jsonify({'success': False, 'message': 'Content required'}), 400
    
    if not recipient_id and not project_id:
        return jsonify({'success': False, 'message': 'Recipient or project required'}), 400
    
    message = Message(
        content=content,
        sender_id=current_user.id,
        recipient_id=recipient_id,
        project_id=project_id
    )
    
    try:
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message_id': message.id,
            'timestamp': message.created_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        print(f"Send message error: {e}")
        return jsonify({'success': False, 'message': 'Failed to send'}), 500

@bp.route('/history/<int:user_id>')
@login_required
def get_history(user_id):
    """Get chat history (AJAX endpoint)"""
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    return jsonify({
        'messages': [{
            'id': m.id,
            'content': m.content,
            'sender_id': m.sender_id,
            'sender_name': m.sender.name,
            'created_at': m.created_at.isoformat(),
            'is_own': m.sender_id == current_user.id
        } for m in messages]
    })
