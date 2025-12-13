"""
ResearchHub AI - Project Management Routes
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Project, User, project_members
from datetime import datetime
from sqlalchemy import and_

bp = Blueprint('project', __name__, url_prefix='/project')

@bp.route('/')
@login_required
def index():
    """List all user projects"""
    # Owned projects
    owned = current_user.owned_projects.order_by(Project.updated_at.desc()).all()
    
    # Member projects
    member_of = current_user.projects.order_by(Project.updated_at.desc()).all()
    
    return render_template('project/index.html',
                         owned_projects=owned,
                         member_projects=member_of)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new project"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        abstract = request.form.get('abstract', '').strip()
        keywords = request.form.get('keywords', '').strip()
        project_type = request.form.get('project_type', 'Solo')
        
        if not title:
            flash('Project title is required.', 'danger')
            return render_template('project/create.html')
        
        project = Project(
            title=title,
            abstract=abstract,
            keywords=keywords,
            project_type=project_type,
            owner_id=current_user.id,
            status='Draft'
        )
        
        try:
            db.session.add(project)
            db.session.flush()
            
            # Add owner as member with Lead role
            stmt = project_members.insert().values(
                user_id=current_user.id,
                project_id=project.id,
                role='Lead'
            )
            db.session.execute(stmt)
            db.session.commit()
            
            flash('Project created successfully!', 'success')
            return redirect(url_for('project.view', project_id=project.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to create project.', 'danger')
            print(f"Project creation error: {e}")
    
    return render_template('project/create.html')

@bp.route('/<int:project_id>')
@login_required
def view(project_id):
    """View project details"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user is member
    is_member = project.members.filter_by(id=current_user.id).first() is not None
    
    if not is_member and project.owner_id != current_user.id:
        flash('You do not have access to this project.', 'warning')
        return redirect(url_for('project.index'))
    
    # Get member role
    user_role = project.get_member_role(current_user.id)
    
    # Get all members with roles
    members_data = []
    for member in project.members.all():
        role = project.get_member_role(member.id)
        members_data.append({
            'user': member,
            'role': role
        })
    
    return render_template('project/view.html',
                         project=project,
                         is_owner=(project.owner_id == current_user.id),
                         user_role=user_role,
                         members=members_data)

@bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    """Edit project"""
    project = Project.query.get_or_404(project_id)
    
    # Only owner or lead can edit
    user_role = project.get_member_role(current_user.id)
    if project.owner_id != current_user.id and user_role != 'Lead':
        flash('You do not have permission to edit this project.', 'warning')
        return redirect(url_for('project.view', project_id=project_id))
    
    if request.method == 'POST':
        project.title = request.form.get('title', '').strip()
        project.abstract = request.form.get('abstract', '').strip()
        project.keywords = request.form.get('keywords', '').strip()
        project.status = request.form.get('status', 'Draft')
        project.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('project.view', project_id=project_id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update project.', 'danger')
            print(f"Project update error: {e}")
    
    return render_template('project/edit.html', project=project)

@bp.route('/<int:project_id>/invite', methods=['POST'])
@login_required
def invite_member(project_id):
    """Invite member to project"""
    project = Project.query.get_or_404(project_id)
    
    # Only owner can invite
    if project.owner_id != current_user.id:
        return jsonify({'success': False, 'message': 'Only owner can invite members'}), 403
    
    user_id = request.form.get('user_id', type=int)
    role = request.form.get('role', 'Contributor')
    
    user = User.query.get_or_404(user_id)
    
    # Check if already member
    if project.members.filter_by(id=user_id).first():
        return jsonify({'success': False, 'message': 'User is already a member'}), 400
    
    try:
        stmt = project_members.insert().values(
            user_id=user_id,
            project_id=project_id,
            role=role
        )
        db.session.execute(stmt)
        db.session.commit()
        
        flash(f'{user.name} added to project!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Invite error: {e}")
        return jsonify({'success': False, 'message': 'Failed to add member'}), 500

@bp.route('/<int:project_id>/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_member(project_id, user_id):
    """Remove member from project"""
    project = Project.query.get_or_404(project_id)
    
    # Only owner can remove
    if project.owner_id != current_user.id:
        return jsonify({'success': False, 'message': 'Only owner can remove members'}), 403
    
    # Cannot remove owner
    if user_id == project.owner_id:
        return jsonify({'success': False, 'message': 'Cannot remove project owner'}), 400
    
    try:
        stmt = project_members.delete().where(
            and_(
                project_members.c.project_id == project_id,
                project_members.c.user_id == user_id
            )
        )
        db.session.execute(stmt)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Remove error: {e}")
        return jsonify({'success': False, 'message': 'Failed to remove member'}), 500

@bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)
    
    # Only owner can delete
    if project.owner_id != current_user.id:
        flash('Only owner can delete the project.', 'warning')
        return redirect(url_for('project.view', project_id=project_id))
    
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully.', 'success')
        return redirect(url_for('project.index'))
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete project.', 'danger')
        print(f"Delete error: {e}")
        return redirect(url_for('project.view', project_id=project_id))
