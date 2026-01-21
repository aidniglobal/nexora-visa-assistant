from flask import Flask
from config import Config
from flask_migrate import Migrate
import os
from datetime import datetime, timezone

# Use the application's central db instance defined in root-level "models.py"
from models import db

migrate = Migrate()

def create_app(test_config: dict | None = None):
    # Ensure templates are loaded from the project-level 'templates' directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(Config)

    # Allow overriding config for tests
    if test_config:
        app.config.update(test_config)

    # Ensure runtime directories exist (instance and uploads)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        upload_folder = app.config.get('UPLOAD_FOLDER')
        if upload_folder:
            os.makedirs(upload_folder, exist_ok=True)
    except Exception as e:
        print('Could not create instance or upload folders:', e)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(main)

    # Initialize Flask-Login for this app instance
    try:
        from flask_login import LoginManager
        login_manager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            from models import db, User
            return db.session.get(User, int(user_id))
    except Exception as e:
        print('Could not initialize login manager:', e)

    # Register common context processors (company info + now) so templates render in tests
    from datetime import datetime
    @app.context_processor
    def inject_company_info():
        company_info = {
            "name": "Aidni Global LLP",
            "contact_number": "+919879428291",
            "email": "phoenixairticket@gmail.com",
            "address": "Aidni Global LLP, India"
        }
        return dict(company_info=company_info, now=lambda: datetime.now(timezone.utc))

    # Add minimal routes used by templates so URL building doesn't fail in tests
    try:
        from flask import render_template, url_for, redirect
        app.add_url_rule('/', 'index', lambda: render_template('index.html'))
        app.add_url_rule('/residencies', 'residencies', lambda: 'residencies')
        app.add_url_rule('/residency-eligibility', 'residency_eligibility', lambda: 'eligibility')
        app.add_url_rule('/residency-calculator', 'residency_calculator', lambda: 'calculator')
        app.add_url_rule('/consultants', 'consultants', lambda: 'consultants')
        app.add_url_rule('/about', 'about', lambda: render_template('about_us.html'))
        app.add_url_rule('/about_app', 'about_app', lambda: render_template('about_app_copy.html'))
        app.add_url_rule('/upload_resume', 'upload_resume', lambda: render_template('upload_resume.html'))
        app.add_url_rule('/create_cover_letter', 'create_cover_letter', lambda: render_template('create_cover_letter.html'))
        app.add_url_rule('/submit_application', 'submit_application', lambda: render_template('visa_application_form.html'), methods=['GET','POST'])
        app.add_url_rule('/visa-requirements', 'visa_requirements', lambda: render_template('visa_requirements.html'))
        app.add_url_rule('/terms', 'terms', lambda: render_template('terms.html'))
        app.add_url_rule('/privacy', 'privacy', lambda: render_template('privacy.html'))
        app.add_url_rule('/user-agreement', 'user_agreement', lambda: render_template('user_agreement.html'))
        app.add_url_rule('/copyright', 'copyright', lambda: render_template('copyright.html'))
        app.add_url_rule('/login', 'login', lambda: render_template('login.html'), methods=['GET','POST'])
        app.add_url_rule('/register', 'register', lambda: render_template('register.html'), methods=['GET','POST'])
        app.add_url_rule('/dashboard', 'dashboard', lambda: render_template('dashboard.html'))
        # Additional placeholder routes used by templates
        app.add_url_rule('/faq', 'faq', lambda: render_template('faq.html'))
        app.add_url_rule('/profile', 'profile', lambda: render_template('profile.html'))
        app.add_url_rule('/logout', 'logout', lambda: redirect(url_for('login')))
        app.add_url_rule('/inquiry', 'inquiry', lambda: render_template('inquiry.html'), methods=['GET','POST'])
        # Job search routes
        app.add_url_rule('/job-search', 'job_search', lambda: render_template('job_search.html'), methods=['GET','POST'])
        app.add_url_rule('/my-job-applications', 'my_job_applications', lambda: render_template('my_job_applications.html'))

    except Exception:
        pass

    # Try to import top-level routes (from project root app.py) and attach admin routes
    try:
        import importlib.util
        root_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.py'))
        if os.path.exists(root_app_path):
            spec = importlib.util.spec_from_file_location('root_app', root_app_path)
            root_app = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(root_app)
            # Attach admin import & management endpoints if present
            if hasattr(root_app, 'admin_import_visa'):
                app.add_url_rule('/admin/import-visa-requirements', 'admin_import_visa', root_app.admin_import_visa, methods=['GET','POST'])
            if hasattr(root_app, 'admin_visa_manage'):
                app.add_url_rule('/admin/visa-management', 'admin_visa_manage', root_app.admin_visa_manage, methods=['GET','POST'])
            if hasattr(root_app, 'inquiry'):
                app.add_url_rule('/inquiry', 'inquiry', root_app.inquiry, methods=['GET','POST'])
            if hasattr(root_app, 'get_visa_info_route'):
                app.add_url_rule('/get_visa_info', 'get_visa_info_route', root_app.get_visa_info_route, methods=['POST'])
            if hasattr(root_app, 'submit_application'):
                app.add_url_rule('/submit_application', 'submit_application', root_app.submit_application, methods=['GET','POST'])
            # Admin inquiries endpoints
            if hasattr(root_app, 'admin_inquiries'):
                app.add_url_rule('/admin/inquiries', 'admin_inquiries', root_app.admin_inquiries, methods=['GET','POST'])
            if hasattr(root_app, 'admin_respond_inquiry'):
                app.add_url_rule('/admin/inquiries/respond/<int:inq_id>', 'admin_respond_inquiry', root_app.admin_respond_inquiry, methods=['GET','POST'])
            if hasattr(root_app, 'admin_quick_reply'):
                app.add_url_rule('/admin/inquiries/quick_reply/<int:inq_id>', 'admin_quick_reply', root_app.admin_quick_reply, methods=['POST'])
            if hasattr(root_app, 'admin_close_inquiry'):
                app.add_url_rule('/admin/inquiries/close/<int:inq_id>', 'admin_close_inquiry', root_app.admin_close_inquiry, methods=['POST'])
    except Exception as e:
        # Non-fatal; dev environment may not need this
        print('Could not attach root admin routes:', e)

    return app

# Export a default app instance for convenience (used in tests)
app = create_app()
