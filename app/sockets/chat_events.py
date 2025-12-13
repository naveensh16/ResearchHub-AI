"""
ResearchHub AI - SocketIO Chat Events
Real-time messaging support
"""
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import db
from app.models import Message
from datetime import datetime

def register_handlers(socketio):
    """Register SocketIO event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        if current_user.is_authenticated:
            print(f"✅ User {current_user.id} connected to chat")
            emit('connected', {'user_id': current_user.id})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        if current_user.is_authenticated:
            print(f"❌ User {current_user.id} disconnected")
    
    @socketio.on('join_chat')
    def handle_join_chat(data):
        """Join chat room (user or project)"""
        if not current_user.is_authenticated:
            return
        
        room_type = data.get('type')  # 'user' or 'project'
        room_id = data.get('id')
        
        room_name = f"{room_type}_{room_id}"
        join_room(room_name)
        
        print(f"👤 User {current_user.id} joined {room_name}")
        emit('joined_chat', {'room': room_name}, room=room_name)
    
    @socketio.on('leave_chat')
    def handle_leave_chat(data):
        """Leave chat room"""
        if not current_user.is_authenticated:
            return
        
        room_type = data.get('type')
        room_id = data.get('id')
        
        room_name = f"{room_type}_{room_id}"
        leave_room(room_name)
        
        print(f"👋 User {current_user.id} left {room_name}")
    
    @socketio.on('send_message')
    def handle_send_message(data):
        """Send message in real-time"""
        if not current_user.is_authenticated:
            return
        
        content = data.get('content', '').strip()
        recipient_id = data.get('recipient_id')
        project_id = data.get('project_id')
        
        if not content:
            emit('error', {'message': 'Content required'})
            return
        
        # Create message
        message = Message(
            content=content,
            sender_id=current_user.id,
            recipient_id=recipient_id,
            project_id=project_id,
            created_at=datetime.utcnow()
        )
        
        try:
            db.session.add(message)
            db.session.commit()
            
            # Prepare message data
            message_data = {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender_id,
                'sender_name': current_user.name,
                'created_at': message.created_at.isoformat(),
                'is_own': True
            }
            
            # Emit to appropriate room
            if recipient_id:
                # 1-to-1 chat
                room_name = f"user_{recipient_id}"
                emit('new_message', message_data, room=room_name)
                
                # Also emit to sender's room
                sender_room = f"user_{current_user.id}"
                emit('new_message', message_data, room=sender_room)
            
            elif project_id:
                # Project group chat
                room_name = f"project_{project_id}"
                emit('new_message', message_data, room=room_name, include_self=True)
            
            print(f"💬 Message {message.id} sent by user {current_user.id}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Message send error: {e}")
            emit('error', {'message': 'Failed to send message'})
    
    @socketio.on('typing')
    def handle_typing(data):
        """Handle typing indicator"""
        if not current_user.is_authenticated:
            return
        
        room_type = data.get('type')
        room_id = data.get('id')
        is_typing = data.get('is_typing', False)
        
        room_name = f"{room_type}_{room_id}"
        
        emit('user_typing', {
            'user_id': current_user.id,
            'user_name': current_user.name,
            'is_typing': is_typing
        }, room=room_name, include_self=False)
    
    @socketio.on('mark_read')
    def handle_mark_read(data):
        """Mark messages as read"""
        if not current_user.is_authenticated:
            return
        
        message_ids = data.get('message_ids', [])
        
        try:
            Message.query.filter(
                Message.id.in_(message_ids),
                Message.recipient_id == current_user.id
            ).update({'is_read': True}, synchronize_session=False)
            
            db.session.commit()
            emit('messages_marked_read', {'message_ids': message_ids})
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Mark read error: {e}")
