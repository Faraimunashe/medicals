from flask import Blueprint, render_template
from flask_login import login_required
from . import db
from app.models import User, Patient, MedicalHistory
from datetime import datetime, date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    patients = Patient.query.all()
    
    gender_counts = {}
    for patient in patients:
        gender_counts[patient.gender] = gender_counts.get(patient.gender, 0) + 1

    # Age distribution
    current_date = datetime.now()
    age_counts = {}
    for patient in patients:
        # Convert dob to datetime for comparison
        dob_datetime = datetime.combine(patient.dob, datetime.min.time())
        age = (current_date - dob_datetime).days // 365
        age_group = f"{age // 10 * 10}-{age // 10 * 10 + 9}" if age < 100 else "100+"
        age_counts[age_group] = age_counts.get(age_group, 0) + 1
        
    
    medical_histories = MedicalHistory.query.all()

    # Prepare data for temperature trends
    temperature_data = {'dates': [], 'values': []}
    for entry in medical_histories:
        temperature_data['dates'].append(entry.created_at.strftime('%Y-%m-%d'))
        temperature_data['values'].append(entry.temperature)

    # Prepare data for diagnosis frequency
    diagnosis_counts = {}
    for entry in medical_histories:
        diagnosis = entry.diagnosis
        diagnosis_counts[diagnosis] = diagnosis_counts.get(diagnosis, 0) + 1

    # Prepare data for treatment plan distribution
    treatment_counts = {}
    for entry in medical_histories:
        plan = entry.plan
        treatment_counts[plan] = treatment_counts.get(plan, 0) + 1
        
    return render_template('dashboard.html', 
                           gender_counts=gender_counts, 
                           age_counts=age_counts,
                           temperature_data=temperature_data,
                           diagnosis_counts=diagnosis_counts,
                           treatment_counts=treatment_counts
                           )
