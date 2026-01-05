from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, Email
import pytesseract
from PIL import Image

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

# Residency Program Models
class ResidencyProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False, index=True)
    program_name = db.Column(db.String(150), nullable=False)
    residency_type = db.Column(db.String(50), nullable=False)  # Investment, Employment, Skilled Migration, etc.
    description = db.Column(db.Text, nullable=False)
    processing_time = db.Column(db.String(100), nullable=False)
    initial_permit_duration = db.Column(db.String(100), nullable=False)
    path_to_citizenship = db.Column(db.String(100), nullable=False)
    visa_free_countries = db.Column(db.Integer, default=0)
    family_eligible = db.Column(db.Boolean, default=False)
    minimum_investment = db.Column(db.String(100), nullable=True)
    minimum_income = db.Column(db.String(100), nullable=True)
    popular = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    applications = db.relationship('ResidencyApplication', backref='program', lazy=True, cascade='all, delete-orphan')
    saved_by = db.relationship('UserSavedProgram', backref='program', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ResidencyProgram {self.country} - {self.program_name}>'


class ResidencyApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('residency_program.id'), nullable=False)
    status = db.Column(db.String(50), default='Draft')  # Draft, Submitted, Under Review, Approved, Rejected
    progress = db.Column(db.Integer, default=0)  # Percentage progress
    notes = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('residency_applications', lazy=True))
    steps = db.relationship('ApplicationStep', backref='application', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('ResidencyApplicationDocument', backref='application', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ResidencyApplication {self.user_id} - {self.program_id}>'


class ApplicationStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('residency_application.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    estimated_duration = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<ApplicationStep {self.step_name}>'


class ResidencyApplicationDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('residency_application.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)  # Passport, Bank Statement, etc.
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ResidencyApplicationDocument {self.document_type}>'


class UserSavedProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('residency_program.id'), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('saved_programs', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<UserSavedProgram {self.user_id} - {self.program_id}>'


class ResidencyConsultant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    specializations = db.Column(db.String(500), nullable=False)  # Comma-separated countries/programs
    experience_years = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    profile_picture = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    appointments = db.relationship('ConsultantAppointment', backref='consultant', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ResidencyConsultant {self.name}>'


class ConsultantAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    consultant_id = db.Column(db.Integer, db.ForeignKey('residency_consultant.id'), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    status = db.Column(db.String(50), default='Scheduled')  # Scheduled, Completed, Cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('appointments', lazy=True))

    def __repr__(self):
        return f'<ConsultantAppointment {self.user_id} - {self.consultant_id}>'


class ResidencyBlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # Guide, Case Study, News, Tips
    countries = db.Column(db.String(500), nullable=True)  # Comma-separated
    author = db.Column(db.String(150), nullable=False)
    featured_image = db.Column(db.String(255), nullable=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ResidencyBlogPost {self.title}>'