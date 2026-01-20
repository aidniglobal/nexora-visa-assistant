from openpyxl import load_workbook
from openpyxl import Workbook
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Document, UserAgreement, VerifiedDocument, ResidencyApplication, ResidencyProgram, Inquiry
from visa_data import get_visa_info, company_info
from datetime import datetime, timezone
from io import BytesIO
import io
from openpyxl import Workbook  # Importing the openpyxl library to create Excel files
from flask_mail import Mail, Message
from app.europass import create_europass_cv

# Heavy optional libs (WeasyPrint, OCR) are imported lazily in functions to keep lightweight deployments small.
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, FileField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileAllowed
import time
import re

# Optional libraries for parsing documents
try:
    import fitz  # PyMuPDF for PDFs
except Exception:
    fitz = None

try:
    import docx  # python-docx for .docx files
except Exception:
    docx = None

app = Flask(__name__, template_folder="templates")

# Initialize Migrate
migrate = Migrate(app, db)

# Configure app settings
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'docx'}
app.secret_key = 'eafcf00803afe5300d29b09f92de1545'
app.config['UPLOAD_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])
app.config['UPLOAD_PATH'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'  # Set to 'production' when deploying
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Limit to 2MB
# Use environment variables when available (safer for deployments)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('1','true','yes')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('1','true','yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config.get('MAIL_USERNAME'))

mail = Mail(app)

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    address = StringField('Address')
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Profile')

# Initialize database and login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # The route for login

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Updated to use session.get()

def update_agreement(status):
    current_user.agreed_to_terms = status
    db.session.commit()
    flash(f"You have {'agreed to' if status else 'disagreed with'} the terms.")
    return redirect(url_for('dashboard'))

def verify_document(file_path):
    """Run basic verification using OCR if enabled; returns True/False."""
    if not app.config.get('ENABLE_OCR', False):
        # OCR disabled for lightweight deployments
        return False
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(img)

        # Perform verification logic (e.g., check for specific keywords)
        if "valid" in extracted_text.lower():
            verification_passed = True
        else:
            verification_passed = False
        return verification_passed
    except Exception as e:
        print(f"Error processing document: {e}")
        return False  # Return False in case of an error

VERIFIED_UPLOAD_FOLDER = 'uploads/verified_documents'
os.makedirs(VERIFIED_UPLOAD_FOLDER, exist_ok=True)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
PHOTOS_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], 'photos')
os.makedirs(PHOTOS_FOLDER, exist_ok=True)

# Specific allowed types for resumes and photos
RESUME_ALLOWED = {'pdf'}
PHOTO_ALLOWED = {'png', 'jpg', 'jpeg'}


def parse_resume(file_path):
    """Parse text from PDF resumes. Only PDFs are supported for resume uploads."""
    text = ""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf' and fitz:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
        else:
            # No parser available for non-PDFs in this flow
            text = ''
    except Exception as e:
        print('parse_resume error:', e)
        text = ''

    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group(0) if email_match else ''
    name = ''
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:10]:
        if line.lower().startswith('name'):
            name = line.split(':',1)[1].strip() if ':' in line else ''
            break
    if not name:
        for line in lines[:10]:
            if '@' not in line and 'resume' not in line.lower() and len(line.split())<=6:
                name = line
                break
    return {'text': text, 'name': name, 'email': email}


def validate_photo(photo_file):
    """Validate passport photo: extension, size (<=200KB), and approximate portrait aspect ratio."""
    if not photo_file or photo_file.filename == '':
        return False, 'No photo uploaded.'
    filename = secure_filename(photo_file.filename)
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext not in PHOTO_ALLOWED:
        return False, 'Photo must be a PNG or JPG image.'

    # Check size
    photo_file.stream.seek(0, 2)
    size = photo_file.stream.tell()
    photo_file.stream.seek(0)
    if size > 200 * 1024:
        return False, 'Photo must be <= 200KB.'

    # Validate aspect ratio
    try:
        img = Image.open(photo_file.stream)
        w, h = img.size
        ratio = w / h
        if not (0.6 <= ratio <= 0.9):
            return False, 'Photo should be portrait (approximate passport dimensions).'
        photo_file.stream.seek(0)
    except Exception as e:
        print('Photo validation error:', e)
        return False, 'Invalid image file.'

    return True, None


@app.route('/upload_resume', methods=['GET','POST'])
@login_required
def upload_resume():
    if request.method == 'POST':
        # Photo is required for both manual entry and file uploads
        photo = request.files.get('photo')
        valid_photo, photo_err = validate_photo(photo)
        if not valid_photo:
            flash(photo_err)
            return redirect(request.url)

        # Save photo
        photo_filename = secure_filename(photo.filename)
        photo_save_path = os.path.join(PHOTOS_FOLDER, photo_filename)
        photo.save(photo_save_path)

        file = request.files.get('file')
        if file and file.filename != '':
            # Resume upload path (PDF only)
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.',1)[1].lower() if '.' in filename else ''
            if ext not in RESUME_ALLOWED or file.mimetype != 'application/pdf':
                flash('Resume must be a PDF file (<=2MB).')
                return redirect(request.url)

            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            parsed = parse_resume(save_path)
            # Pre-fill name/email if parsed, otherwise empty
            return render_template('upload_resume.html', parsed=parsed, filename=filename, photo=photo_filename)
        else:
            # Manual entry path: accept name/email from form
            name = request.form.get('name','').strip()
            email = request.form.get('email','').strip()
            if not name or not email:
                flash('If you did not upload a resume, provide Name and Email in the form.')
                return redirect(request.url)
            parsed = {'text': '', 'name': name, 'email': email}
            return render_template('upload_resume.html', parsed=parsed, filename=None, photo=photo_filename)

    return render_template('upload_resume.html', parsed=None)


@app.route('/generate_europass', methods=['POST'])
@login_required
def generate_europass():
    name = request.form.get('name','').strip()
    email = request.form.get('email','').strip()
    photo_filename = request.form.get('photo_filename') or request.files.get('photo_filename')

    if not name or not email:
        flash('Name and email are required to generate Europass CV.')
        return redirect(url_for('upload_resume'))

    # If photo_filename isn't provided as text, try to get from form file
    photo_path = None
    photo_file = request.files.get('photo')
    if photo_file and photo_file.filename:
        ok, err = validate_photo(photo_file)
        if not ok:
            flash(err)
            return redirect(url_for('upload_resume'))
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(PHOTOS_FOLDER, photo_filename)
        photo_file.save(photo_path)
    elif photo_filename:
        photo_path = os.path.join(PHOTOS_FOLDER, secure_filename(photo_filename))
        if not os.path.exists(photo_path):
            photo_path = None

    if not photo_path:
        flash('Passport photo is required to generate the Europass CV.')
        return redirect(url_for('upload_resume'))

    user_data = {'name': name, 'email': email}
    try:
        output_path = create_europass_cv(user_data, photo_path=photo_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        print('Error generating Europass:', e)
        flash('Error generating Europass CV.')
        return redirect(url_for('upload_resume'))


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/verify-document', methods=['GET', 'POST'])
@login_required
def verify_document_route():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Simulating document verification process
            verification_passed = True  # Replace with actual verification logic

            if verification_passed:
                file.save(file_path)

                # Save document details to the database
                new_document = Document(
                    filename=filename,
                    filepath=file_path,
                    user_id=current_user.id
                )
                db.session.add(new_document)
                db.session.commit()

                flash('Document verified and uploaded successfully!')
                return redirect(url_for('dashboard'))  # Redirect to dashboard or any relevant page
            else:
                flash('Document verification failed.')
                return redirect(request.url)

    return render_template('verify.html')  # Template for the document verification page

@app.route('/agree')
def agree():
    return update_agreement(True)

@app.route('/disagree')
def disagree():
    return update_agreement(False)

# Global context processor to pass company_info to all templates
@app.context_processor
def inject_company_info():
    company_info = {
        "name": "Aidni Global LLP",
        "contact_number": "+919879428291",
        "email": "phoenixairticket@gmail.com",
        "address": "Aidni Global LLP, India"
    }
    # Expose company info and a `now()` helper to templates
    return dict(company_info=company_info, now=lambda: datetime.now(timezone.utc))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about_us.html')  # Ensure you have the corresponding template

@app.route('/terms')
def terms():
    return render_template('terms.html')  # Ensure you have a corresponding template for this route

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Assuming you have password hashing
            login_user(user)  # Log the user in
            next_page = request.args.get('next')  # Redirect to the page the user was trying to access before login
            return redirect(next_page or url_for('dashboard'))  # Redirect to the dashboard or the next page

        flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user  # Use current_user directly
    if user:
        # Fetch all documents associated with the logged-in user
        files = user.documents  # Assuming you have a relationship between User and Document
        return render_template('dashboard.html', files=files, user_details=user)  # Pass user_details explicitly
    else:
        flash("No user found", "danger")
        return redirect(url_for('login'))
    

@app.route('/create_cover_letter', methods=['GET','POST'])
@login_required
def create_cover_letter():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        recipient = request.form.get('recipient','').strip()
        company = request.form.get('company','').strip()
        position = request.form.get('position','').strip()
        opening = request.form.get('opening','').strip()
        body = request.form.get('body','').strip()
        closing = request.form.get('closing','').strip()

        if not all([name, email, recipient, company, position]):
            flash('Please fill in required fields: Name, Email, Recipient, Company, Position')
            return redirect(request.url)

        applicant = {'name': name, 'email': email}
        try:
            from app.europass import create_cover_letter as _create_cover
            output_path = _create_cover(applicant, recipient, company, position, opening, body, closing)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            print('Error generating cover letter:', e)
            flash('Error generating cover letter.')
            return redirect(request.url)

    return render_template('create_cover_letter.html')


# Visa requirements pages
from app.visa_requirements import list_countries, list_visa_types, get_requirements, reload_seed


@app.route('/visa-requirements')
def visa_requirements():
    country = request.args.get('country')
    visa_type = request.args.get('visa_type')

    countries = list_countries()

    data = get_requirements(country=country, visa_type=visa_type) if (country or visa_type) else get_requirements()

    # We'll pass countries list, selected country, selected visa type and requirements data
    return render_template('visa_requirements.html', countries=countries, selected_country=country, selected_visa_type=visa_type, data=data)


@app.route('/api/visa-requirements')
def api_visa_requirements():
    country = request.args.get('country')
    visa_type = request.args.get('visa_type')
    data = get_requirements(country=country, visa_type=visa_type)
    return jsonify(data)


@app.route('/admin/import-visa-requirements', methods=['GET','POST'])
@login_required
def admin_import_visa():
    # Simple admin check
    if not getattr(current_user, 'is_admin', False):
        return render_template('admin_import_visa.html', countries=[])

    # show countries list on GET
    countries = list_countries()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Validate JSON structure
        try:
            import json
            data = json.load(file)
        except Exception as e:
            flash('Invalid JSON file')
            return redirect(request.url)

        # Validate structure using script helper
        try:
            from scripts.import_visa_requirements import validate_structure
            ok, err = validate_structure(data)
            if not ok:
                flash(f'Invalid schema: {err}')
                return redirect(request.url)
        except Exception as e:
            flash('Validation routine not available')
            return redirect(request.url)

        # Write to seed and reload
        try:
            # Write to the canonical seed path used by app.visa_requirements
            try:
                from app.visa_requirements import SEED_PATH as seed_path
            except Exception:
                seed_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'visa_requirements_seed.json'))
            os.makedirs(os.path.dirname(seed_path), exist_ok=True)
            with open(seed_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # Reload in-memory representation
            try:
                reload_seed()
            except Exception:
                pass
            flash('Visa requirements imported successfully')
            return redirect(url_for('visa_requirements'))
        except Exception as e:
            print('Import error:', e)
            flash('Error writing seed file')
            return redirect(request.url)

    return render_template('admin_import_visa.html', countries=countries)


@app.route('/admin/visa-management', methods=['GET','POST'])
@login_required
def admin_visa_manage():
    # admin UI to view countries and restore defaults
    if not getattr(current_user, 'is_admin', False):
        return render_template('admin_visa_manage.html', countries=[])

    from app.visa_requirements import list_countries, restore_default_seed
    countries = list_countries()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'restore':
            restored = restore_default_seed()
            if restored is None:
                flash('Failed to restore default seed')
            else:
                flash('Default seed restored successfully')
            return redirect(url_for('admin_visa_manage'))
        elif action == 'download':
            try:
                from app.visa_requirements import SEED_PATH as seed_path
            except Exception:
                seed_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'visa_requirements_seed.json'))
            if os.path.exists(seed_path):
                return send_file(seed_path, as_attachment=True)
            else:
                flash('Seed file not found')
                return redirect(url_for('admin_visa_manage'))

    return render_template('admin_visa_manage.html', countries=countries)


# ---------------- Admin: inquiries ----------------
@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    if not getattr(current_user, 'is_admin', False):
        flash('Unauthorized', 'danger')
        return redirect(url_for('index'))
    status = request.args.get('status')  # optional filter
    page = int(request.args.get('page', 1))
    per_page = 5
    query = Inquiry.query
    if status == 'unresponded':
        query = query.filter(Inquiry.response == None, Inquiry.status == 'open')
    elif status == 'closed':
        query = query.filter(Inquiry.status == 'closed')
    pagination = query.order_by(Inquiry.created_at.asc()).paginate(page=page, per_page=per_page, error_out=False)
    inquiries = pagination.items
    return render_template('admin_inquiries.html', inquiries=inquiries, filter_status=status, pagination=pagination)


@app.route('/admin/inquiries/respond/<int:inq_id>', methods=['GET','POST'])
@login_required
def admin_respond_inquiry(inq_id):
    if not getattr(current_user, 'is_admin', False):
        flash('Unauthorized', 'danger')
        return redirect(url_for('index'))
    from flask import abort
    inq = db.session.get(Inquiry, inq_id)
    if not inq:
        abort(404)
    if request.method == 'POST':
        response = request.form.get('response','').strip()
        if not response:
            flash('Response cannot be empty', 'danger')
            return redirect(request.url)
        inq.response = response
        inq.responded_at = datetime.now(timezone.utc)
        inq.responded_by = current_user.id
        inq.status = 'responded'
        db.session.commit()
        # Email using template
        try:
            if not app.config.get('TESTING', False):
                # render email body from templates
                body = render_template('emails/inquiry_response.txt', inquiry=inq, response=response)
                html = render_template('emails/inquiry_response.html', inquiry=inq, response=response)
                send_email(inq.email, f'Response to your inquiry', body=body, html_content=html)
        except Exception as e:
            print('Could not send response email:', e)
        flash('Response saved and sent', 'success')
        return redirect(url_for('admin_inquiries'))
    return render_template('admin_respond.html', inquiry=inq)


@app.route('/admin/inquiries/quick_reply/<int:inq_id>', methods=['POST'])
@login_required
def admin_quick_reply(inq_id):
    if not getattr(current_user, 'is_admin', False):
        return ('Unauthorized', 403)
    from flask import abort
    inq = db.session.get(Inquiry, inq_id)
    if not inq:
        abort(404)
    # Create a quick templated response
    response = render_template('emails/inquiry_response.txt', inquiry=inq, response='')
    inq.response = response
    inq.responded_at = datetime.now(timezone.utc)
    inq.responded_by = current_user.id
    inq.status = 'responded'
    db.session.commit()
    # Send email
    try:
        if not app.config.get('TESTING', False):
            body = response
            html = render_template('emails/inquiry_response.html', inquiry=inq, response=response)
            send_email(inq.email, f'Response to your inquiry', body=body, html_content=html)
    except Exception as e:
        print('Could not send quick reply email:', e)
    return ('OK', 200)


@app.route('/admin/inquiries/close/<int:inq_id>', methods=['POST'])
@login_required
def admin_close_inquiry(inq_id):
    if not getattr(current_user, 'is_admin', False):
        return ('Unauthorized', 403)
    from flask import abort
    inq = db.session.get(Inquiry, inq_id)
    if not inq:
        abort(404)
    inq.status = 'closed'
    inq.closed_at = datetime.now(timezone.utc)
    db.session.commit()
    return ('OK', 200)

def user_agreement():
    agreement_text = """
    By uploading your documents, you agree to allow Aidni Global LLP to use your documents
    solely for the purpose of processing visa applications. Your data will be handled
    securely and in compliance with applicable laws.
    """

    if request.method == 'POST':
        # Check if agreement already exists
        existing_agreement = UserAgreement.query.filter_by(user_id=current_user.id).first()
        if not existing_agreement:
            new_agreement = UserAgreement(
                user_id=current_user.id,
                agreement_text=agreement_text,
                agreed_at=datetime.now(timezone.utc),
                status=True
            )
            db.session.add(new_agreement)
        else:
            existing_agreement.agreed_at = datetime.now(timezone.utc)
            existing_agreement.status = True

        db.session.commit()

        # Generate PDF agreement
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(current_user.name))
        os.makedirs(user_folder, exist_ok=True)
        pdf_path = os.path.join(user_folder, f"user_agreement_{current_user.id}.pdf")
        # Prefer WeasyPrint if available/enabled, otherwise fall back to a simple FPDF-based PDF
        try:
            if app.config.get('ENABLE_WEASYPRINT', False):
                from weasyprint import HTML
                HTML(string=agreement_text).write_pdf(pdf_path)
            else:
                # Fallback: simple PDF using fpdf
                try:
                    from fpdf import FPDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font('Arial', size=11)
                    for line in agreement_text.splitlines():
                        pdf.multi_cell(0, 6, txt=line)
                    pdf.output(pdf_path)
                except Exception as e:
                    # As a last resort, write plain text to .pdf so the file exists
                    with open(pdf_path, 'wb') as f:
                        f.write(agreement_text.encode('utf-8', errors='replace'))
        except Exception as e:
            print('Could not generate agreement PDF:', e)

        flash("Thank you for agreeing to the terms. A copy has been saved.", "success")
        return redirect(url_for('dashboard'))

    return render_template('user_agreement.html', agreement_text=agreement_text)

def generate_pdf(content, filename):
    """Generate a PDF from HTML content using WeasyPrint if available, otherwise fallback to a simple FPDF output."""
    try:
        if app.config.get('ENABLE_WEASYPRINT', False):
            from weasyprint import HTML
            html = HTML(string=content)
            pdf = html.write_pdf()
            with open(filename, 'wb') as f:
                f.write(pdf)
        else:
            # Simple fallback: strip html tags and write text using FPDF
            try:
                from fpdf import FPDF
                import re
                text = re.sub('<[^<]+?>', '', content)
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font('Arial', size=11)
                for line in text.splitlines():
                    pdf.multi_cell(0, 6, txt=line)
                pdf.output(filename)
            except Exception as e:
                # Fallback to plain text file if all else fails
                with open(filename, 'wb') as f:
                    f.write(content.encode('utf-8', errors='replace'))
    except Exception as e:
        print('generate_pdf failed:', e)
        with open(filename, 'wb') as f:
            f.write(content.encode('utf-8', errors='replace'))



@app.route('/inquiry', methods=['GET','POST'])
def inquiry():
    from models import Inquiry
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        message = request.form.get('message','').strip()
        if not (name and email and message):
            flash('Please provide name, email, and a message.')
            return redirect(request.url)
        user_id = current_user.id if getattr(current_user, 'is_authenticated', False) else None
        inq = Inquiry(user_id=user_id, name=name, email=email, message=message)
        db.session.add(inq)
        db.session.commit()
        # Try to notify via email in non-testing environments; non-fatal
        if not app.config.get('TESTING', False):
            try:
                send_email(app.config.get('MAIL_DEFAULT_SENDER'), f'New inquiry from {name}', body=message)
            except Exception as e:
                print('Could not send inquiry notification:', e)
        flash('Your inquiry has been received; our team will contact you shortly.', 'success')
        return redirect(url_for('index'))

    # Prefill if logged in
    if getattr(current_user, 'is_authenticated', False):
        return render_template('inquiry.html', name=current_user.name, email=current_user.email)
    return render_template('inquiry.html')

@app.route('/upload_document', methods=['GET', 'POST'])
@login_required
def upload_document():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
            os.makedirs(user_folder, exist_ok=True)
            filepath = os.path.join(user_folder, filename)
            file.save(filepath)

            # Save document to the database
            document = Document(filename=filename, filepath=filepath, user_id=current_user.id)
            db.session.add(document)
            db.session.commit()

            flash("Your document was uploaded successfully and is now available in your dashboard.", "success")
            return redirect(url_for('dashboard'))

        flash("Invalid file type. Allowed types: png, jpg, jpeg, pdf", "danger")
    return render_template('upload_document.html')  # Ensure template has progress bar logic


# User Profile Management Route
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    form = ProfileForm(obj=user)  # Pre-populate form with user data
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.address = form.address.data

        # Handle profile picture upload
        if form.profile_picture.data:
            picture = form.profile_picture.data
            filename = secure_filename(picture.filename)
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            picture.save(picture_path)

            # Update user's profile picture path
            user.profile_picture = filename

        db.session.commit()  # Save changes to database
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', form=form, user=user)


# Email Notification Placeholder
def send_email(recipient, subject, body=None, html_content=None):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    if body:
        msg.body = body
    if html_content:
        msg.html = html_content
    mail.send(msg)



@app.route('/download/<int:doc_id>')
@login_required
def download(doc_id):
    from flask import abort
    document = db.session.get(Document, doc_id)
    if not document:
        abort(404)
    if document.user_id != current_user.id:
        flash('You are not authorized to access this file.')
        return redirect(url_for('dashboard'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], document.filename)

@app.route('/delete/<int:doc_id>')
@login_required
def delete_document(doc_id):
    from flask import abort
    document = db.session.get(Document, doc_id)

    if not document:
        abort(404)

    # Check if the current user owns the document
    if document.user_id != current_user.id:
        flash('You are not authorized to delete this file.', 'danger')
        return redirect(url_for('dashboard'))

    # Check if the file exists before trying to delete
    if os.path.exists(document.filepath):
        try:
            os.remove(document.filepath)  # Attempt to delete the file
        except Exception as e:
            flash(f"An error occurred while deleting the file: {str(e)}", 'danger')
            return redirect(url_for('dashboard'))
    else:
        flash('File not found on the server. It might have already been deleted.', 'warning')

    # Delete the document record from the database
    db.session.delete(document)
    db.session.commit()
    flash('File deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/submit_application', methods=['GET', 'POST'])
def submit_application():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        nationality = request.form['nationality']
        passport_number = request.form['passport_number']
        passport_expiry = request.form['passport_expiry']
        marital_status = request.form['marital_status']
        address = request.form['address']
        contact_number = request.form['contact_number']
        email = request.form['email']
        visa_type = request.form['visa_type']
        country = request.form['country']
        arrival_date = request.form['arrival_date']
        duration_of_stay = request.form['duration_of_stay']
        occupation = request.form.get('occupation', '')
        employer_name = request.form.get('employer_name', '')
        employer_address = request.form.get('employer_address', '')
        education_qualification = request.form.get('education_qualification', '')
        institution_name = request.form.get('institution_name', '')
        course_name = request.form.get('course_name', '')

        # Handle file uploads
        uploaded_files = {
            "passport_copy": request.files.get('passport_copy'),
            "education_docs": request.files.get('education_docs'),
            "employment_letters": request.files.get('employment_letters'),
            "bank_statements": request.files.get('bank_statements'),
            "proof_accommodation": request.files.get('proof_accommodation'),
        }

        # Create a unique folder for each submission (using timestamp or name)
        timestamp = int(time.time())  # Use timestamp to create a unique folder
        submission_folder = os.path.join(app.config['UPLOAD_FOLDER'], f"submission_{timestamp}")
        
        if not os.path.exists(submission_folder):
            os.makedirs(submission_folder)

        # Save uploaded files into the submission folder
        for file_key, file_obj in uploaded_files.items():
            if file_obj:
                filename = secure_filename(file_obj.filename)
                file_obj.save(os.path.join(submission_folder, filename))

        # Prepare data for PDF rendering
        pdf_data = {
            'name': name,
            'gender': gender,
            'dob': dob,
            'nationality': nationality,
            'passport_number': passport_number,
            'passport_expiry': passport_expiry,
            'marital_status': marital_status,
            'address': address,
            'contact_number': contact_number,
            'email': email,
            'visa_type': visa_type,
            'country': country,
            'arrival_date': arrival_date,
            'duration_of_stay': duration_of_stay,
            'occupation': occupation,
            'employer_name': employer_name,
            'employer_address': employer_address,
            'education_qualification': education_qualification,
            'institution_name': institution_name,
            'course_name': course_name
        }

        # Render the HTML template for PDF
        html = render_template('visa_application_form.html', **pdf_data)

        # Generate PDF and save it in the submission folder
        pdf_filename = f"{name.replace(' ', '_')}_visa_application.pdf"
        pdf_path = os.path.join(submission_folder, pdf_filename)
        HTML(string=html).write_pdf(pdf_path)

        flash(f'Visa application submitted successfully! Your submission has been saved in {submission_folder}.', 'success')
        return redirect(url_for('index'))  # Redirect to the home page or confirmation page

    return render_template('visa_application_form.html')

@app.route('/get_visa_info', methods=['POST'])
def get_visa_info_route():
    country = request.form.get('country')
    visa_type = request.form.get('visa_type')
    documents = get_visa_info(country, visa_type)
    return render_template('index.html', documents=documents, country=country, visa_type=visa_type, company_info=company_info)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check for missing fields
        if not name:
            flash('Name is required')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered')
            return redirect(url_for('register'))

        # Create new user and set password
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Check if the user has accepted the terms and conditions
        accepted_terms = request.form.get('accepted_terms')  # Assuming this checkbox exists in the form
        if accepted_terms:
            agreement = UserAgreement(user_id=new_user.id, agreement_text="User Agreement Text Here", accepted=True)
            db.session.add(agreement)
            db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


# ==================== RESIDENCY ROUTES ====================

@app.route('/residencies')
def residencies():
    """Browse all residency programs"""
    from residency_data import get_all_countries
    countries = get_all_countries()
    return render_template('residencies.html', countries=countries)


@app.route('/residencies/<country>')
def residency_country(country):
    """View residency programs for a specific country"""
    from residency_data import residency_programs, get_programs_by_country
    
    if country not in residency_programs:
        flash(f'Country {country} not found')
        return redirect(url_for('residencies'))
    
    programs = residency_programs[country]
    return render_template('residency_country.html', country=country, programs=programs)


@app.route('/residencies/<country>/<program_name>')
def residency_program_detail(country, program_name):
    """View details of a specific residency program"""
    from residency_data import residency_programs
    
    if country not in residency_programs:
        flash('Country not found')
        return redirect(url_for('residencies'))
    
    if program_name not in residency_programs[country]:
        flash('Program not found')
        return redirect(url_for('residency_country', country=country))
    
    program = residency_programs[country][program_name]
    saved = False
    if current_user.is_authenticated:
        from models import UserSavedProgram
        saved = UserSavedProgram.query.filter_by(
            user_id=current_user.id,
            program_id=program_name  # Using program name as identifier
        ).first() is not None
    
    return render_template('residency_detail.html', country=country, program_name=program_name, program=program, saved=saved)


@app.route('/residency-comparison', methods=['GET', 'POST'])
def residency_comparison():
    """Compare multiple residency programs"""
    from residency_data import residency_programs
    
    selected_programs = []
    if request.method == 'POST':
        program_ids = request.form.getlist('selected_programs')
        for program_id in program_ids:
            parts = program_id.split('::')
            if len(parts) == 2:
                country, program_name = parts
                if country in residency_programs and program_name in residency_programs[country]:
                    selected_programs.append({
                        'country': country,
                        'name': program_name,
                        'data': residency_programs[country][program_name]
                    })
    
    all_countries = list(residency_programs.keys())
    return render_template('residency_comparison.html', 
                          all_countries=all_countries, 
                          selected_programs=selected_programs)


@app.route('/residency-filter', methods=['POST'])
def residency_filter():
    """Filter residency programs by criteria"""
    from residency_data import residency_programs, filter_programs
    
    filters = {
        'residency_type': request.form.get('residency_type'),
        'max_investment': request.form.get('max_investment'),
        'citizenship_available': request.form.get('citizenship_available') == 'on'
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None and v != 'on' and v != ''}
    
    if filters.get('max_investment'):
        filters['max_investment'] = int(filters['max_investment'])
    
    results = filter_programs(filters)
    
    return render_template('residency_filter_results.html', results=results, filters=filters)


@app.route('/residency-calculator')
def residency_calculator():
    """ROI and cost calculator for residency programs"""
    return render_template('residency_calculator.html')


@app.route('/api/calculate-roi', methods=['POST'])
def calculate_roi():
    """API endpoint for ROI calculations"""
    data = request.get_json()
    investment = float(data.get('investment', 0))
    annual_return_percent = float(data.get('annual_return', 5))
    years = int(data.get('years', 5))
    
    roi = investment * ((1 + annual_return_percent/100) ** years)
    total_profit = roi - investment
    
    return {
        'initial_investment': investment,
        'final_value': round(roi, 2),
        'total_profit': round(total_profit, 2),
        'years': years
    }


@app.route('/residency-eligibility')
def residency_eligibility():
    """Eligibility checker for residency programs"""
    return render_template('residency_eligibility.html')


@app.route('/api/check-eligibility', methods=['POST'])
def check_eligibility():
    """API endpoint for eligibility checking"""
    from residency_data import residency_programs
    
    data = request.get_json()
    investment_budget = float(data.get('investment_budget', 0))
    income = float(data.get('income', 0))
    citizenship_wanted = data.get('citizenship_wanted') == 'true'
    preferred_countries = data.get('preferred_countries', [])
    
    eligible_programs = []
    
    for country in preferred_countries if preferred_countries else residency_programs.keys():
        if country not in residency_programs:
            continue
        
        for program_name, program_data in residency_programs[country].items():
            eligibility_score = 100
            reasons = []
            
            # Check investment
            if 'investment_types' in program_data:
                min_investment = None
                for inv_type, inv_data in program_data['investment_types'].items():
                    amount_str = inv_data['minimum'].replace('€', '').replace('£', '').replace('CAD $', '').replace('AUD $', '').replace('AED ', '').replace('SGD $', '').replace('/year', '').replace(',', '').strip()
                    try:
                        amount = float(amount_str)
                        if min_investment is None or amount < min_investment:
                            min_investment = amount
                    except:
                        pass
                
                if min_investment and investment_budget < min_investment:
                    eligibility_score -= 30
                    reasons.append(f"Investment requirement: ${min_investment:,.0f}")
            
            # Check income
            if program_data.get('minimum_income'):
                income_str = program_data['minimum_income'].replace('€', '').replace('$', '').replace('/month', '').replace(',', '').strip()
                try:
                    min_income = float(income_str)
                    if income < min_income * 12:
                        eligibility_score -= 20
                        reasons.append(f"Income requirement: ${min_income:,.0f}/month")
                except:
                    pass
            
            # Check citizenship path
            if citizenship_wanted:
                if 'No citizenship path' in program_data.get('path_to_citizenship', ''):
                    eligibility_score -= 40
                    reasons.append("No citizenship path available")
                else:
                    reasons.append(f"Citizenship: {program_data.get('path_to_citizenship', 'N/A')}")
            
            if eligibility_score >= 50:
                eligible_programs.append({
                    'country': country,
                    'program': program_name,
                    'score': max(0, eligibility_score),
                    'reasons': reasons
                })
    
    # Sort by eligibility score
    eligible_programs.sort(key=lambda x: x['score'], reverse=True)
    
    return {'eligible_programs': eligible_programs[:10]}


@app.route('/save-program', methods=['POST'])
@login_required
def save_program():
    """Save a residency program to user's favorites"""
    from models import UserSavedProgram
    
    country = request.form.get('country')
    program_name = request.form.get('program_name')
    
    # Check if already saved
    existing = UserSavedProgram.query.filter_by(
        user_id=current_user.id
    ).first()
    
    if not existing:
        saved = UserSavedProgram(
            user_id=current_user.id,
            program_id=f"{country}::{program_name}"
        )
        db.session.add(saved)
        db.session.commit()
        flash('Program saved successfully!', 'success')
    else:
        flash('Program already saved', 'info')
    
    return redirect(request.referrer or url_for('residencies'))


@app.route('/my-residency-applications')
@login_required
def my_residency_applications():
    """View user's residency applications"""
    from models import ResidencyApplication
    
    applications = ResidencyApplication.query.filter_by(user_id=current_user.id).all()
    return render_template('my_residency_applications.html', applications=applications)


@app.route('/consultants')
def consultants():
    """View available consultants"""
    from models import ResidencyConsultant
    
    page = request.args.get('page', 1, type=int)
    specialization = request.args.get('specialization')
    
    query = ResidencyConsultant.query.filter_by(verified=True)
    if specialization:
        query = query.filter(ResidencyConsultant.specializations.contains(specialization))
    
    consultants_list = query.order_by(ResidencyConsultant.rating.desc()).paginate(page=page, per_page=12)
    
    return render_template('consultants.html', consultants=consultants_list)


@app.route('/consultant/<int:consultant_id>')
def consultant_profile(consultant_id):
    """View consultant profile"""
    from models import ResidencyConsultant
    from flask import abort
    consultant = db.session.get(ResidencyConsultant, consultant_id)
    if not consultant:
        abort(404)
    return render_template('consultant_profile.html', consultant=consultant)


@app.route('/book-consultation', methods=['GET', 'POST'])
@login_required
def book_consultation():
    """Book a consultation with a consultant"""
    from models import ResidencyConsultant, ConsultantAppointment
    
    if request.method == 'POST':
        consultant_id = request.form.get('consultant_id')
        scheduled_at = request.form.get('scheduled_at')
        duration = request.form.get('duration', 30)
        notes = request.form.get('notes')
        
        consultant = db.session.get(ResidencyConsultant, consultant_id)
        from flask import abort
        if not consultant:
            abort(404)
        try:
            from datetime import datetime
            scheduled_datetime = datetime.fromisoformat(scheduled_at)
            
            appointment = ConsultantAppointment(
                user_id=current_user.id,
                consultant_id=consultant_id,
                scheduled_at=scheduled_datetime,
                duration_minutes=int(duration),
                notes=notes
            )
            db.session.add(appointment)
            db.session.commit()
            
            flash('Consultation booked successfully!', 'success')
            return redirect(url_for('my_residency_applications'))
        except Exception as e:
            flash(f'Error booking consultation: {str(e)}', 'danger')
    
    consultants_list = ResidencyConsultant.query.filter_by(verified=True).all()
    return render_template('book_consultation.html', consultants=consultants_list)

@app.route('/about-app')
def about_app():
    """Render a copyable About text for sharing and embedding"""
    try:
        with open('about_app_copy.md', 'r') as f:
            about_text = f.read()
    except Exception:
        about_text = "Nexora — Global Residency & Visa Platform\nVisit: http://localhost:5000"
    return render_template('about_app_copy.html', about_text=about_text)


@app.route('/about-us')
def about_us():
    """Render About Us page with copy/share functionality"""
    try:
        with open('about_app_copy.md', 'r') as f:
            about_text = f.read()
    except Exception:
        about_text = "Nexora — Global Residency & Visa Platform\nVisit: http://localhost:5000"
    return render_template('about_us_share.html', about_text=about_text)


@app.route('/copyright')
def copyright():
    return render_template('copyright.html')


if __name__ == '__main__':
    # Ensure the database and tables are created
    if app.config['ENV'] == 'development':
        with app.app_context():
            db.create_all()

    # Create the upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
