from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from . import db
from app.models import Patient, MedicalHistory
from app.forms import PatientForm
from datetime import datetime
import random
import string

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    search_query = request.args.get('search', '')
    if search_query:
        # Use a case-insensitive search
        patients = Patient.query.filter(
            (Patient.reference.ilike(f'%{search_query}%')) |
            (Patient.firstnames.ilike(f'%{search_query}%')) |
            (Patient.surname.ilike(f'%{search_query}%')) |
            (Patient.email.ilike(f'%{search_query}%')) |
            (Patient.phone.ilike(f'%{search_query}%'))
        ).all()
    else:
        patients = Patient.query.all()
        
    form = PatientForm()
    return render_template('patients.html', patients=patients, form=form, search_query=search_query)



def generate_random_code():
    number_part = f"{random.randint(0, 9999):04d}"
    letter_part = random.choice(string.ascii_uppercase)
    random_code = f"PT{number_part}{letter_part}"
    
    return random_code


@patients_bp.route('/patients/new', methods=['GET', 'POST'])
def create_patient():
    form = PatientForm()
    if form.validate_on_submit():
        print("ggg")
        new_patient = Patient(
            reference=generate_random_code(),
            firstnames=form.firstnames.data,
            surname=form.surname.data,
            gender=form.gender.data,
            email=form.email.data,
            phone=form.phone.data,
            dob=form.dob.data,
            address=form.address.data,
            created_at=datetime.now()
        )
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient created successfully!')
        return redirect(url_for('patients.patients'))
    # else:
    #     print(form.errors)
    #     flash('error An error occured please try again!')
    return render_template('patients/create_patient.html', form=form)


@patients_bp.route('/patients/<int:id>', methods=['GET'])
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    medicals = MedicalHistory.query.filter_by(patient_id=id).all()
    return render_template('patients/view_patient.html', patient=patient, medicals=medicals)

@patients_bp.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)
    
    if form.validate_on_submit():
        patient.firstnames = form.firstnames.data
        patient.surname = form.surname.data
        patient.gender = form.gender.data
        patient.email = form.email.data,
        patient.phone = form.phone.data
        patient.dob = form.dob.data
        patient.address = form.address.data
        
        db.session.commit()
        flash('Patient updated successfully!')
        return redirect(url_for('patients.patients'))
    
    return render_template('patients/edit_patient.html', form=form, patient=patient)

@patients_bp.route('/patients/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'danger')
    return redirect(url_for('patients.patients'))