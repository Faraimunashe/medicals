from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField, DateField, DateTimeField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp, Optional, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
#import datetime
from app.models import Branch, User
from datetime import datetime

class BranchForm(FlaskForm):
    name = StringField('Branch Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Branch Name"})
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@company.com", "autofocus": True, "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField('Login Account')
   

class UserForm(FlaskForm):
    role = SelectField('Role', choices=[(2, 'Clerk'), (1, 'Admin')], validators=[DataRequired()]) 
    branch = QuerySelectField('Branch', query_factory=lambda: Branch.query.all(), get_label='name', allow_blank=False, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit') 

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


zimbabwe_phone_regex = r'^07\d{8}$'

def validate_dob(form, field):
    if field.data > datetime.today().date():
        raise ValidationError('Date of Birth must be less than or equal to today.')

class PatientForm(FlaskForm):
    firstnames = StringField('First Names', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    phone = StringField('Phone Number (without country code)', validators=[
        DataRequired(), 
        Regexp(zimbabwe_phone_regex, message="Phone number must be a valid Zimbabwe mobile number")
    ])
    dob = DateField('Date of Birth', validators=[DataRequired(), validate_dob])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Submit')


class MedicalHistoryForm(FlaskForm):
    branch = QuerySelectField('Branch', query_factory=lambda: Branch.query.all(), get_label='name', allow_blank=False, validators=[DataRequired()])
    reference = StringField('Patient Reference', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Reference Code"})
    temperature = DecimalField('Temperature (°C)', validators=[DataRequired(), NumberRange(min=30, max=45)])
    bp = StringField('Blood Pressure', validators=[DataRequired(), Regexp(r'\d{2,3}/\d{2,3}', message="BP format should be like 120/80")])
    description = StringField('Description', validators=[DataRequired()])
    diagnosis = StringField('Diagnosis', validators=[DataRequired()])
    plan = StringField('Plan', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class AppointmentForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    reference = StringField('Patient Reference', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Reference Code"})
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    notes = TextAreaField('Notes (Optional)')
    submit = SubmitField('Schedule Appointment')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.doctor_id.choices = [(doc.id, doc.name) for doc in User.query.filter_by(role=2).all()]  # Role 2 is for doctors
        self.branch_id.choices = [(branch.id, branch.name) for branch in Branch.query.all()]
