from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Portfolio
from forms import RegistrationForm, LoginForm, PortfolioForm
import json
import os
from datetime import datetime
import zipfile
import io

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
Session(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', portfolio=portfolio)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        portfolio = Portfolio(
            user_id=current_user.id,
            name=form.name.data,
            bio=form.bio.data,
            skills=json.dumps([skill.strip() for skill in form.skills.data.split('\n') if skill.strip()]),
            education=json.dumps([edu.strip() for edu in form.education.data.split('\n') if edu.strip()]),
            projects=json.dumps([proj.strip() for proj in form.projects.data.split('\n') if proj.strip()]),
            social_links=json.dumps([link.strip() for link in form.social_links.data.split('\n') if link.strip()])
        )
        
        try:
            db.session.add(portfolio)
            db.session.commit()
            flash('Portfolio created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your portfolio.', 'danger')
    
    return render_template('form.html', form=form)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_portfolio():
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not portfolio:
        flash('No portfolio found. Please create one first.', 'warning')
        return redirect(url_for('create_portfolio'))
    
    form = PortfolioForm(obj=portfolio)
    if form.validate_on_submit():
        portfolio.name = form.name.data
        portfolio.bio = form.bio.data
        portfolio.skills = json.dumps([skill.strip() for skill in form.skills.data.split('\n') if skill.strip()])
        portfolio.education = json.dumps([edu.strip() for edu in form.education.data.split('\n') if edu.strip()])
        portfolio.projects = json.dumps([proj.strip() for proj in form.projects.data.split('\n') if proj.strip()])
        portfolio.social_links = json.dumps([link.strip() for link in form.social_links.data.split('\n') if link.strip()])
        portfolio.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Portfolio updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your portfolio.', 'danger')
    
    # Pre-fill form with existing data
    form.name.data = portfolio.name
    form.bio.data = portfolio.bio
    form.skills.data = '\n'.join(json.loads(portfolio.skills))
    form.education.data = '\n'.join(json.loads(portfolio.education))
    form.projects.data = '\n'.join(json.loads(portfolio.projects))
    form.social_links.data = '\n'.join(json.loads(portfolio.social_links))
    
    return render_template('form.html', form=form)

@app.route('/preview/<username>')
def preview_portfolio(username):
    user = User.query.filter_by(username=username).first_or_404()
    portfolio = Portfolio.query.filter_by(user_id=user.id).first_or_404()
    
    data = {
        'name': portfolio.name,
        'bio': portfolio.bio,
        'skills': json.loads(portfolio.skills),
        'education': json.loads(portfolio.education),
        'projects': json.loads(portfolio.projects),
        'social_links': json.loads(portfolio.social_links)
    }
    
    return render_template('portfolio.html', data=data)

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        # Get form data
        data = {
            'name': request.form.get('name', ''),
            'title': request.form.get('title', ''),
            'bio': request.form.get('bio', ''),
            'skills': [skill.strip() for skill in request.form.get('skills', '').split(',') if skill.strip()],
            'education': [],
            'projects': [],
            'contact': {
                'email': request.form.get('email', ''),
                'github': request.form.get('github', ''),
                'linkedin': request.form.get('linkedin', ''),
                'instagram': request.form.get('instagram', '')
            }
        }
        
        # Process education entries
        courses = request.form.getlist('course[]')
        years = request.form.getlist('year[]')
        institutes = request.form.getlist('institute[]')
        
        for i in range(len(courses)):
            if courses[i] and years[i] and institutes[i]:
                data['education'].append({
                    'course': courses[i],
                    'year': years[i],
                    'institute': institutes[i]
                })
        
        # Process project entries
        project_names = request.form.getlist('project_name[]')
        project_descriptions = request.form.getlist('project_description[]')
        project_links = request.form.getlist('project_link[]')
        project_tech = request.form.getlist('project_tech[]')
        
        for i in range(len(project_names)):
            if project_names[i] and project_descriptions[i]:
                data['projects'].append({
                    'name': project_names[i],
                    'description': project_descriptions[i],
                    'link': project_links[i] if project_links[i] else '#',
                    'tech': project_tech[i] if project_tech[i] else ''
                })
        
        # Store data in session
        session['portfolio_data'] = data
        
        return render_template('portfolio.html', data=data)
    else:
        # If it's a GET request, check if we have data in session
        if 'portfolio_data' in session:
            return render_template('portfolio.html', data=session['portfolio_data'])
        return redirect(url_for('home'))

@app.route('/download')
def download():
    if 'portfolio_data' not in session:
        return redirect(url_for('home'))
    
    # Generate HTML content
    html_content = render_template('portfolio.html', data=session['portfolio_data'])
    
    # Create a ZIP file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # Add the HTML file
        zf.writestr('portfolio.html', html_content)
        
        # Add static files
        static_dir = os.path.join(app.root_path, 'static')
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, static_dir)
                zf.write(file_path, arcname)
    
    memory_file.seek(0)
    
    # Generate filename
    filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )

@app.route('/theme/<theme>')
def set_theme(theme):
    session['theme'] = theme
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True) 