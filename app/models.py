from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from app import db
from datetime import date

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='branch', lazy=True)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'<Branch {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [user.id for user in self.users]
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Integer)

    def __init__(self, branch_id, email, password, name, role):
        self.branch_id = branch_id
        self.email = email
        self.password = password
        self.name = name
        self.role = role
        
    def __repr__(self):
        return f'<User {self.name}, Branch: {self.branch.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "branch_id": self.branch_id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
        }

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), nullable=False, unique=True)
    firstnames = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __init__(self, reference, firstnames, surname, gender, email, phone, address, dob, created_at):
        self.reference = reference
        self.firstnames = firstnames
        self.surname = surname
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.dob = dob
        self.created_at = created_at

    @property
    def full_name(self):
        return f"{self.firstnames} {self.surname}"

    def to_dict(self):
        return {
            "id": self.id,
            "reference": self.reference,
            "firstnames": self.firstnames,
            "surname": self.surname,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "dob": self.dob.isoformat(),
            "created_at": self.created_at.isoformat(),
            "full_name": self.full_name
        }

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    branch_id = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    bp = db.Column(db.String(7), nullable=False)
    description = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    plan = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    
    def __init__(self, patient_id, branch_id, temperature, bp, description, diagnosis, plan, created_at):
        self.patient_id = patient_id
        self.branch_id = branch_id
        self.temperature = temperature
        self.bp = bp
        self.description = description
        self.diagnosis = diagnosis
        self.plan = plan
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "branch_id": self.branch_id,
            "temperature": self.temperature,
            "bp": self.bp,
            "description": self.description,
            "diagnosis": self.diagnosis,
            "plan": self.plan,
            "created_at": self.created_at.isoformat(),
        }

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='Scheduled')
    notes = db.Column(db.Text)

    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='appointments')
    branch = db.relationship('Branch', backref='appointments')

    def __repr__(self):
        return f'<Appointment {self.id} for {self.patient.full_name} with Dr. {self.doctor.name} at {self.branch.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "branch_id": self.branch_id,
            "appointment_date": self.appointment_date.isoformat(),
            "appointment_time": self.appointment_time.isoformat(),
            "status": self.status,
            "notes": self.notes,
            "patient_name": self.patient.full_name if self.patient else None,
            "doctor_name": self.doctor.name if self.doctor else None,
            "branch_name": self.branch.name if self.branch else None
        }

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100))
    model_id = db.Column(db.Integer)
    action = db.Column(db.String(50))
    previous_data = db.Column(db.JSON)
    new_data = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, model_name, model_id, action, previous_data, new_data, user_id):
        self.model_name = model_name
        self.model_id = model_id
        self.action = action
        self.previous_data = previous_data
        self.new_data = new_data
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "model_name": self.model_name,
            "model_id": self.model_id,
            "action": self.action,
            "previous_data": self.previous_data,
            "new_data": self.new_data,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id
        }
