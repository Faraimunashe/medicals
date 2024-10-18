from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.Integer)

    def __init__(self, email, password, name, role):
        self.email = email
        self.password = password
        self.name = name
        self.role = role

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstnames = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)

    def __init__(self, firstnames, surname, gender, phone, address, dob, created_at):
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

# For other models like Sale, define them similarly, ensuring that
# db and datetime are imported correctly and models are initialized
