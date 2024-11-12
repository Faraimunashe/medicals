from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file
from flask_login import login_required
from . import db
from app.models import Patient, MedicalHistory
from app.forms import MedicalHistoryForm
from datetime import datetime
from app.audit_helper import log_create, log_update, log_delete
from app.predict import from_symptoms
from sqlalchemy import asc, desc
import pandas as pd
from io import BytesIO

medicals_bp = Blueprint('medicals', __name__)

@medicals_bp.route('/medicals', methods=['GET'])
@login_required
def medicals():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'id')  
    sort_order = request.args.get('sort_order', 'asc') 

    order = asc(sort_by) if sort_order == 'asc' else desc(sort_by)
    
    query = db.session.query(MedicalHistory, Patient).join(Patient, MedicalHistory.patient_id == Patient.id)

    if search_query:
        query = query.filter(
            (MedicalHistory.description.ilike(f'%{search_query}%')) |
            (MedicalHistory.diagnosis.ilike(f'%{search_query}%')) |
            (MedicalHistory.plan.ilike(f'%{search_query}%'))
        )
    
    medicals = query.order_by(order).all()

    return render_template('medicals.html', medicals=medicals, search_query=search_query, sort_by=sort_by, sort_order=sort_order)

@medicals_bp.route('/medicals/new', methods=['GET', 'POST'])
def create_medicals():
    form = MedicalHistoryForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(reference=form.reference.data).first()
        if not patient:
            flash('Incorrect patient ref#!')
            return redirect(url_for('medicals.create_medicals'))
        branch = form.branch.data
        print(patient.to_dict())
        diags = from_symptoms(form.description.data)
        new_medical_history = MedicalHistory(
            patient_id= patient.id,
            branch_id=branch.id,
            temperature=form.temperature.data,
            bp=form.bp.data,
            description=form.description.data,
            diagnosis=diags,
            plan=form.plan.data,
            created_at=datetime.now()
        )
        
        db.session.add(new_medical_history)
        db.session.commit()
        log_create(new_medical_history)
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
    medical_history_old = medical_history
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
        log_update(medical_history, medical_history_old)
        flash('Medicals updated successfully!')
        return redirect(url_for('medicals.medicals'))
    
    return render_template('medicals/update_medical.html', form=form, medical_history=medical_history)


@medicals_bp.route('/medicals/delete/<int:id>', methods=['POST'])
def delete_medicals(id):
    medical_history = MedicalHistory.query.get_or_404(id)
    
    try:
        db.session.delete(medical_history)
        db.session.commit()
        log_delete(medical_history)
        flash('Medicals deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the medical history. Please try again.')

    return redirect(url_for('medicals.medicals'))


@medicals_bp.route('/export_medicals', methods=['GET'])
@login_required
def export_medicals():
   
    search_query = request.args.get('search', '')
    query = db.session.query(MedicalHistory, Patient).join(Patient, MedicalHistory.patient_id == Patient.id)

    if search_query:
        query = query.filter(
            (MedicalHistory.description.ilike(f'%{search_query}%')) |
            (MedicalHistory.diagnosis.ilike(f'%{search_query}%')) |
            (MedicalHistory.plan.ilike(f'%{search_query}%'))
        )
    
    results = query.all()

    data = []
    for medical, patient in results:
        data.append({
            "Record ID": medical.id,
            "Patient Reference": patient.reference,
            "Temperature": medical.temperature,
            "Blood Pressure": medical.bp,
            "Description": medical.description,
            "Diagnosis": medical.diagnosis,
            "Plan": medical.plan,
            "Created At": medical.created_at
        })

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MedicalRecords')

    output.seek(0)
    return send_file(output, as_attachment=True, download_name='MedicalRecords.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

