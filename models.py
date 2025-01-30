from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
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
    agreed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
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
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('verified_documents', lazy=True))

    def __repr__(self):
        return f'<VerifiedDocument {self.filename} - Status: {self.status}>'

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

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('visa_applications', lazy=True))

    def __repr__(self):
        return f'<VisaApplication {self.visa_type} - {self.country} - {self.user_id}>'
