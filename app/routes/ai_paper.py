"""
ResearchHub AI - AI Paper Generator Routes (KILLER FEATURE)
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_login import login_required, current_user
from app import db
from app.models import Paper, Project, AIReview
from datetime import datetime
import json
from io import BytesIO

# Try to import WeasyPrint (requires GTK on Windows)
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"⚠️  WeasyPrint not available: {e}")
    print("   PDF export will not work. Install GTK runtime to enable.")

# Lazy import AI service to avoid initialization errors in serverless
try:
    from app.services.ai_service import AIService
    ai_service = AIService()
    AI_AVAILABLE = True
except Exception as e:
    print(f"⚠️  AI Service not available: {e}")
    ai_service = None
    AI_AVAILABLE = False

bp = Blueprint('ai_paper', __name__, url_prefix='/paper')

@bp.route('/')
@login_required
def index():
    """List all papers"""
    papers = current_user.papers.order_by(Paper.updated_at.desc()).all()
    return render_template('paper/index.html', papers=papers)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new paper (AI-assisted)"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        domain = request.form.get('domain', '').strip()
        keywords = request.form.get('keywords', '').strip()
        objective = request.form.get('objective', '').strip()
        method_type = request.form.get('method_type', '').strip()
        project_id = request.form.get('project_id', type=int)
        
        if not title:
            flash('Paper title is required.', 'danger')
            return render_template('paper/create.html')
        
        paper = Paper(
            title=title,
            domain=domain,
            keywords=keywords,
            objective=objective,
            method_type=method_type,
            author_id=current_user.id,
            project_id=project_id,
            status='Draft'
        )
        
        try:
            db.session.add(paper)
            db.session.commit()
            flash('Paper created! Now generate AI sections.', 'success')
            return redirect(url_for('ai_paper.generate', paper_id=paper.id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to create paper.', 'danger')
            print(f"Paper creation error: {e}")
    
    # Get user projects for dropdown
    projects = current_user.projects.all()
    return render_template('paper/create.html', projects=projects)

@bp.route('/<int:paper_id>')
@login_required
def view(paper_id):
    """View paper"""
    paper = Paper.query.get_or_404(paper_id)
    
    # Check access
    if paper.author_id != current_user.id:
        # Check if user is in paper's project
        if paper.project:
            is_member = paper.project.members.filter_by(id=current_user.id).first()
            if not is_member:
                flash('You do not have access to this paper.', 'warning')
                return redirect(url_for('ai_paper.index'))
        else:
            flash('You do not have access to this paper.', 'warning')
            return redirect(url_for('ai_paper.index'))
    
    return render_template('paper/view.html', paper=paper)

@bp.route('/<int:paper_id>/generate', methods=['GET', 'POST'])
@login_required
def generate(paper_id):
    """AI Generate paper sections"""
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.author_id != current_user.id:
        flash('You do not have permission to edit this paper.', 'warning')
        return redirect(url_for('ai_paper.view', paper_id=paper_id))
    
    if request.method == 'POST':
        sections = request.form.getlist('sections')
        
        if not sections:
            flash('Please select at least one section to generate.', 'warning')
            return render_template('paper/generate.html', paper=paper)
        
        # Check if AI service is available
        if not AI_AVAILABLE or ai_service is None:
            flash('AI service is not available. Please configure AI provider.', 'danger')
            return render_template('paper/generate.html', paper=paper)
        
        try:
            # Generate sections using AI
            generated_content = ai_service.generate_paper_sections(
                title=paper.title,
                domain=paper.domain,
                keywords=paper.keywords,
                objective=paper.objective,
                method_type=paper.method_type,
                sections=sections
            )
            
            # Update paper with generated content
            for section, content in generated_content.items():
                setattr(paper, section, content)
            
            paper.ai_generated = True
            paper.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Sections generated successfully! Review and edit as needed.', 'success')
            return redirect(url_for('ai_paper.edit', paper_id=paper_id))
            
        except Exception as e:
            flash(f'AI generation failed: {str(e)}', 'danger')
            print(f"AI generation error: {e}")
    
    return render_template('paper/generate.html', paper=paper)

@bp.route('/<int:paper_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(paper_id):
    """Edit paper sections"""
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.author_id != current_user.id:
        flash('You do not have permission to edit this paper.', 'warning')
        return redirect(url_for('ai_paper.view', paper_id=paper_id))
    
    if request.method == 'POST':
        # Update all sections
        paper.title = request.form.get('title', '').strip()
        paper.abstract = request.form.get('abstract', '').strip()
        paper.introduction = request.form.get('introduction', '').strip()
        paper.problem_statement = request.form.get('problem_statement', '').strip()
        paper.literature_review = request.form.get('literature_review', '').strip()
        paper.methodology = request.form.get('methodology', '').strip()
        paper.results = request.form.get('results', '').strip()
        paper.conclusion = request.form.get('conclusion', '').strip()
        paper.future_work = request.form.get('future_work', '').strip()
        paper.references = request.form.get('references', '').strip()
        paper.status = request.form.get('status', 'Draft')
        paper.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Paper updated successfully!', 'success')
            return redirect(url_for('ai_paper.view', paper_id=paper_id))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update paper.', 'danger')
            print(f"Paper update error: {e}")
    
    return render_template('paper/edit.html', paper=paper)

@bp.route('/<int:paper_id>/improve', methods=['POST'])
@login_required
def improve_section(paper_id):
    """AI improve specific section"""
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.author_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    data = request.get_json()
    section = data.get('section')
    current_text = data.get('text', '')
    
    if not section:
        return jsonify({'success': False, 'message': 'Section required'}), 400
    
    # Check if AI service is available
    if not AI_AVAILABLE or ai_service is None:
        return jsonify({'success': False, 'message': 'AI service not available'}), 503
    
    try:
        improved_text = ai_service.improve_text(
            section_name=section,
            current_text=current_text,
            context={
                'title': paper.title,
                'domain': paper.domain,
                'objective': paper.objective
            }
        )
        
        return jsonify({
            'success': True,
            'improved_text': improved_text
        })
    except Exception as e:
        print(f"Improvement error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/<int:paper_id>/review')
@login_required
def review(paper_id):
    """AI review paper for issues"""
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.author_id != current_user.id:
        flash('You do not have permission to review this paper.', 'warning')
        return redirect(url_for('ai_paper.view', paper_id=paper_id))
    
    # Check if AI service is available
    if not AI_AVAILABLE or ai_service is None:
        flash('AI service is not available. Please configure AI provider.', 'danger')
        return redirect(url_for('ai_paper.view', paper_id=paper_id))
    
    try:
        # Run AI review
        review_results = ai_service.review_paper(paper)
        
        # Store review results
        paper.review_feedback = json.dumps(review_results)
        paper.last_reviewed = datetime.utcnow()
        
        # Create AIReview records for tracking
        for finding in review_results.get('findings', []):
            ai_review = AIReview(
                paper_id=paper.id,
                review_type=finding.get('type'),
                findings=json.dumps(finding),
                severity=finding.get('severity', 'medium')
            )
            db.session.add(ai_review)
        
        db.session.commit()
        
        return render_template('paper/review.html',
                             paper=paper,
                             review_results=review_results)
    except Exception as e:
        flash(f'AI review failed: {str(e)}', 'danger')
        print(f"Review error: {e}")
        return redirect(url_for('ai_paper.view', paper_id=paper_id))

@bp.route('/<int:paper_id>/delete', methods=['POST'])
@login_required
def delete(paper_id):
    """Delete paper"""
    paper = Paper.query.get_or_404(paper_id)
    
    if paper.author_id != current_user.id:
        flash('You do not have permission to delete this paper.', 'warning')
        return redirect(url_for('ai_paper.view', paper_id=paper_id))
    
    try:
        db.session.delete(paper)
        db.session.commit()
        flash('Paper deleted successfully.', 'success')
        return redirect(url_for('ai_paper.index'))
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete paper.', 'danger')
        print(f"Delete error: {e}")
        return redirect(url_for('ai_paper.view', paper_id=paper_id))

@bp.route('/<int:paper_id>/export')
@login_required
def export_paper(paper_id):
    """Export paper to PDF with conference formatting"""
    
    # Get format from query parameter
    format_type = request.args.get('format', 'ieee')
    
    paper = Paper.query.get_or_404(paper_id)
    
    # Check access
    if paper.author_id != current_user.id:
        if paper.project:
            is_member = paper.project.members.filter_by(id=current_user.id).first()
            if not is_member:
                flash('You do not have access to this paper.', 'warning')
                return redirect(url_for('ai_paper.index'))
        else:
            flash('You do not have access to this paper.', 'warning')
            return redirect(url_for('ai_paper.index'))
    
    # Validate format
    valid_formats = ['ieee', 'acm', 'springer']
    if format_type not in valid_formats:
        flash('Invalid export format.', 'danger')
        return redirect(url_for('ai_paper.view', paper_id=paper_id))
    
    try:
        # Select template based on format
        template_name = f'paper/paper_{format_type}.html'
        
        # Render HTML with paper content
        html_content = render_template(
            template_name,
            paper=paper,
            current_year=datetime.now().year
        )
        
        # Try PDF generation if WeasyPrint is available
        if WEASYPRINT_AVAILABLE:
            try:
                # Generate PDF from HTML
                pdf_buffer = BytesIO()
                HTML(string=html_content).write_pdf(pdf_buffer)
                pdf_buffer.seek(0)
                
                # Create response
                response = make_response(pdf_buffer.getvalue())
                response.headers['Content-Type'] = 'application/pdf'
                
                # Clean filename
                safe_title = "".join(c for c in paper.title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '_')[:50]
                filename = f"{safe_title}_{format_type.upper()}.pdf"
                
                response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                return response
            except Exception as pdf_error:
                print(f"PDF generation failed: {pdf_error}, falling back to HTML")
        
        # Fallback: Return formatted HTML for browser printing
        # Add print instructions to the HTML
        print_instructions = """
        <div style="position: fixed; top: 10px; right: 10px; background: #4F46E5; color: white; 
                    padding: 15px 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
                    z-index: 1000; font-family: Arial, sans-serif;">
            <strong>📄 {format_name} Format Ready!</strong><br/>
            <small>Press <strong>Ctrl+P</strong> to save as PDF</small>
            <button onclick="window.print()" 
                    style="margin-top: 10px; background: white; color: #4F46E5; border: none; 
                           padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold;">
                🖨️ Print Now
            </button>
            <style>@media print {{ div {{ display: none !important; }} }}</style>
        </div>
        """.format(format_name=format_type.upper())
        
        html_with_instructions = html_content.replace('</body>', print_instructions + '</body>')
        
        return html_with_instructions
        
    except Exception as e:
        flash(f'Failed to export paper: {str(e)}', 'danger')
        print(f"Export error: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('ai_paper.view', paper_id=paper_id))

