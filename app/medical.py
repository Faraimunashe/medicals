from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from . import db
from app.models import Patient, MedicalHistory
from app.forms import MedicalHistoryForm
from datetime import datetime
import random
import string

medicals_bp = Blueprint('medicals', __name__)

@medicals_bp.route('/medicals', methods=['GET'])
@login_required
def medicals():
    search_query = request.args.get('search', '')
    if search_query:
        # Use a case-insensitive search
        patients = MedicalHistory.query.filter(
            (MedicalHistory.description.ilike(f'%{search_query}%')) |
            (MedicalHistory.diagnosis.ilike(f'%{search_query}%')) |
            (MedicalHistory.plan.ilike(f'%{search_query}%'))
        ).all()
    else:
        medicals = MedicalHistory.query.all()
        
    return render_template('medicals.html', medicals=medicals, search_query=search_query)



@medicals_bp.route('/medicals/new', methods=['GET', 'POST'])
def create_medicals():
    form = MedicalHistoryForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(reference=form.reference.data).first()
        branch = form.branch.data
        new_medical_history = MedicalHistory(
            patient_id= patient.id,
            branch_id=branch.id,
            temperature=form.temperature.data,
            bp=form.bp.data,
            description=form.description.data,
            diagnosis=form.diagnosis.data,
            plan=form.plan.data,
            created_at=datetime.now()
        )
        
        db.session.add(new_medical_history)
        db.session.commit()
        flash('Medicals created successfully!')
        return redirect(url_for('medicals.medicals'))
   
    return render_template('medicals/create_medical.html', form=form)



@medicals_bp.route('/medicals/<int:id>', methods=['GET'])
def view_medical(id):
    medical = MedicalHistory.query.get_or_404(id)
    patient = Patient.query.get_or_404(medical.patient_id)
    return render_template('medicals/view_medical.html', patient=patient, medical=medical)


@medicals_bp.route('/medicals/update/<int:id>', methods=['GET', 'POST'])
def update_medicals(id):
    medical_history = MedicalHistory.query.get_or_404(id)
    form = MedicalHistoryForm(obj=medical_history)
    
    if form.validate_on_submit():
        patient = Patient.query.filter_by(reference=form.reference.data).first()
        branch = form.branch.data
        
        medical_history.patient_id= patient.id
        medical_history.branch_id=branch.id
        medical_history.temperature = form.temperature.data
        medical_history.bp = form.bp.data
        medical_history.description = form.description.data
        medical_history.diagnosis = form.diagnosis.data
        medical_history.plan = form.plan.data
        db.session.commit()
        flash('Medicals updated successfully!')
        return redirect(url_for('medicals.medicals'))
    
    return render_template('medicals/update_medical.html', form=form, medical_history=medical_history)


@medicals_bp.route('/medicals/delete/<int:id>', methods=['POST'])
def delete_medicals(id):
    medical_history = MedicalHistory.query.get_or_404(id)
    
    try:
        db.session.delete(medical_history)
        db.session.commit()
        flash('Medicals deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the medical history. Please try again.')

    return redirect(url_for('medicals.medicals'))
