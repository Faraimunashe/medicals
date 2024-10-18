from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
import datetime


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "example@company.com", "autofocus": True, "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField('Login Account')
    

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


zimbabwe_phone_regex = r'^07\d{8}$'

class PatientForm(FlaskForm):
    firstnames = StringField('First Names', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    phone = StringField('Phone Number (without country code)', validators=[
        DataRequired(), 
        Regexp(zimbabwe_phone_regex, message="Phone number must be a valid Zimbabwe mobile number")
    ])
    dob = DateField('DOB', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    
    submit = SubmitField('Submit')     
