"""
ResearchHub AI - Database Models
"""
from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association Tables
project_members = db.Table('project_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('role', db.String(20), default='Contributor'),  # Lead, Contributor
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

collaboration_requests = db.Table('collaboration_requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('receiver_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('status', db.String(20), default='pending'),  # pending, accepted, rejected
    db.Column('message', db.Text),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(UserMixin, db.Model):
    """User model for researchers"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(200))
    bio = db.Column(db.Text)
    research_domains = db.Column(db.Text)  # Comma-separated tags
    current_interests = db.Column(db.Text)
    availability = db.Column(db.String(20), default='Solo')  # Solo, Team
    role = db.Column(db.String(20), default='User')  # User, Admin
    avatar_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = db.relationship('Project', secondary=project_members, 
                             back_populates='members', lazy='dynamic')
    owned_projects = db.relationship('Project', backref='owner', 
                                    foreign_keys='Project.owner_id', lazy='dynamic')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                   backref='sender', lazy='dynamic')
    papers = db.relationship('Paper', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def get_domains_list(self):
        """Get research domains as list"""
        if self.research_domains:
            return [d.strip() for d in self.research_domains.split(',') if d.strip()]
        return []
    
    def __repr__(self):
        return f'<User {self.email}>'

class Project(db.Model):
    """Research project model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(500))  # Comma-separated
    project_type = db.Column(db.String(20), default='Solo')  # Solo, Team
    status = db.Column(db.String(20), default='Draft')  # Draft, Active, Completed
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('User', secondary=project_members,
                            back_populates='projects', lazy='dynamic')
    papers = db.relationship('Paper', backref='project', lazy='dynamic')
    messages = db.relationship('Message', backref='project', lazy='dynamic')
    
    def get_keywords_list(self):
        """Get keywords as list"""
        if self.keywords:
            return [k.strip() for k in self.keywords.split(',') if k.strip()]
        return []
    
    def get_member_role(self, user_id):
        """Get user role in project"""
        result = db.session.execute(
            db.select(project_members.c.role).where(
                db.and_(
                    project_members.c.project_id == self.id,
                    project_members.c.user_id == user_id
                )
            )
        ).first()
        return result[0] if result else None
    
    def __repr__(self):
        return f'<Project {self.title}>'

class Paper(db.Model):
    """Research paper model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    domain = db.Column(db.String(100))
    keywords = db.Column(db.String(500))
    objective = db.Column(db.Text)
    method_type = db.Column(db.String(100))
    
    # Paper sections
    abstract = db.Column(db.Text)
    introduction = db.Column(db.Text)
    problem_statement = db.Column(db.Text)
    literature_review = db.Column(db.Text)
    methodology = db.Column(db.Text)
    results = db.Column(db.Text)  # Results and Discussion section
    conclusion = db.Column(db.Text)
    future_work = db.Column(db.Text)
    references = db.Column(db.Text)
    
    # Metadata
    status = db.Column(db.String(20), default='Draft')  # Draft, Review, Final
    ai_generated = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # AI Review
    review_feedback = db.Column(db.Text)  # JSON stored as text
    last_reviewed = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Paper {self.title}>'

class Message(db.Model):
    """Chat message model"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # For 1-to-1
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))  # For group chat
    message_type = db.Column(db.String(20), default='text')  # text, file, system
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Message from User:{self.sender_id}>'

class AIReview(db.Model):
    """AI paper review tracking"""
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False)
    review_type = db.Column(db.String(50))  # structure, clarity, logic, completeness
    findings = db.Column(db.Text)  # JSON stored as text
    severity = db.Column(db.String(20))  # low, medium, high, critical
    status = db.Column(db.String(20), default='pending')  # pending, addressed, ignored
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    paper = db.relationship('Paper', backref='reviews')
    
    def __repr__(self):
        return f'<AIReview for Paper:{self.paper_id}>'
