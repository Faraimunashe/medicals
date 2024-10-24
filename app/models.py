from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from app import db
from datetime import date

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'<Branch {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, nullable=False)
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
        

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), nullable=False, unique=True)
    firstnames = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __init__(self, reference, firstnames, surname, gender, phone, address, dob, created_at):
        self.reference = reference
        self.firstnames = firstnames
        self.surname = surname
        self.gender = gender
        self.phone = phone
        self.address = address
        self.dob = dob
        self.created_at = created_at

    @property
    def full_name(self):
        return f"{self.firstnames} {self.surname}"

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    branch_id = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    bp = db.Column(db.String(7), nullable=False)
    description = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    plan = db.Column(db.Text, nullable=False)
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