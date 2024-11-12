from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField, DateField, DateTimeField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp, Optional, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
#import datetime
from app.models import Branch, User, Appointment
from datetime import datetime, date, time, timedelta

class BranchForm(FlaskForm):
    name = StringField('Branch Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Branch Name"})
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@company.com", "autofocus": True, "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField('Login Account')
   

class UserForm(FlaskForm):
    role = SelectField('Role', choices=[(3, 'Nurse'),(2, 'Doctor'), (1, 'Admin')], validators=[DataRequired()]) 
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
    email = StringField('Email', validators=[DataRequired(), Email()])
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
    diagnosis = StringField('Diagnosis')
    plan = StringField('Plan')
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
        self.doctor_id.choices = [(doc.id, doc.name) for doc in User.query.filter_by(role=2).all()]
        self.branch_id.choices = [(branch.id, branch.name) for branch in Branch.query.all()]

    def validate_appointment_date(self, appointment_date):
        today = date.today()
        if appointment_date.data < today:
            raise ValidationError("The appointment date cannot be in the past.")

    def validate_appointment_time(self, appointment_time):
        today = date.today()
        now = datetime.now().time()
        # Only apply time validation if the selected date is today
        if self.appointment_date.data == today and appointment_time.data <= now:
            raise ValidationError("For appointments scheduled today, the time must be later than the current time.")
    
    def validate_doctor_id(self, doctor_id):
        # Convert form date and time into a single datetime object
        appointment_start = datetime.combine(self.appointment_date.data, self.appointment_time.data)
        restricted_end_time = appointment_start + timedelta(minutes=15)  # Restrict appointments within 15 minutes after the selected time

        # Query for appointments with overlapping times for the same doctor on the same date
        overlapping_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id.data,
            Appointment.appointment_date == self.appointment_date.data,
            Appointment.appointment_time.between(appointment_start.time(), restricted_end_time.time())  # Time falls within the restricted range
        ).all()

        if overlapping_appointments:
            raise ValidationError("This doctor already has an appointment within 15 minutes of the selected time. Please select another time.")