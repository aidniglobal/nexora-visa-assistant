from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, Email
from PIL import Image

# Conditional import for OCR (optional heavy dependency)
try:
    import pytesseract
except ImportError:
    pytesseract = None

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))  # New field for phone number
    address = db.Column(db.String(200))  # New field for address
    profile_picture = db.Column(db.String(120), default='default.jpg')  # Default profile picture
    is_admin = db.Column(db.Boolean, default=False)  # Flag for admin users
    # Resume fields
    full_name = db.Column(db.String(150), nullable=True)
    headline = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    resume_updated_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.name}, {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('documents', lazy=True))

    def __repr__(self):
        return f'<Document {self.filename} (User ID: {self.user_id})>'

class UserAgreement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    agreement_text = db.Column(db.Text, nullable=False)
    agreed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    accepted = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('agreement', uselist=False))

    def __repr__(self):
        return f'<UserAgreement {self.user_id} - Accepted: {self.accepted}>'

class VerifiedDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('verified_documents', lazy=True))

    def __repr__(self):
        return f'<VerifiedDocument {self.filename} - Status: {self.status}>'


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    responded_at = db.Column(db.DateTime, nullable=True)
    responded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(20), default='open')  # open, responded, closed
    closed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('inquiries', lazy=True), foreign_keys=[user_id])
    responder = db.relationship('User', backref=db.backref('responded_inquiries', lazy=True), foreign_keys=[responded_by])

    def __repr__(self):
        return f'<Inquiry {self.name} - {self.email} - {self.status}>'
# New Model for Visa Application Form
class VisaApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visa_type = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    duration_of_stay = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(100), nullable=True)
    employer_name = db.Column(db.String(100), nullable=True)
    employer_address = db.Column(db.String(200), nullable=True)
    education_qualification = db.Column(db.String(100), nullable=True)
    institution_name = db.Column(db.String(200), nullable=True)
    course_name = db.Column(db.String(100), nullable=True)

    # Document relationships
    passport_copy = db.Column(db.String(200), nullable=False)
    education_docs = db.Column(db.String(200), nullable=False)
    employment_letters = db.Column(db.String(200), nullable=False)
    bank_statements = db.Column(db.String(200), nullable=False)
    proof_accommodation = db.Column(db.String(200), nullable=False)

    # Agreement
    terms_accepted = db.Column(db.Boolean, default=False)

    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('visa_applications', lazy=True))

    def __repr__(self):
        return f'<VisaApplication {self.visa_type} - {self.country} - {self.user_id}>'

# Residency Program Models - Moved to investment context
# Keeping minimal model structure for investment applications

class InvestmentApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(200), nullable=True)
    business_type = db.Column(db.String(100), nullable=True)
    investment_amount = db.Column(db.String(50), nullable=True)
    target_country = db.Column(db.String(100), nullable=False)
    program_type = db.Column(db.String(150), nullable=False)
    timeline = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='Pending')  # Pending, Reviewing, Approved, Rejected
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<InvestmentApplication {self.full_name} - {self.program_type}>'

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    job_id = db.Column(db.String(100), nullable=False)  # CareerJet job ID
    job_title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(150), nullable=True)
    job_url = db.Column(db.String(500), nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume_url = db.Column(db.String(500), nullable=True)
    cover_letter = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Applied')  # Applied, Viewed, In Review, Rejected, Accepted
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<JobApplication {self.job_title} @ {self.company}>'