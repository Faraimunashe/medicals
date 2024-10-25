from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from . import db
from app.models import Appointment, Patient, User, Branch
from app.forms import AppointmentForm
from datetime import datetime
from app.notification import send_email

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
@login_required
def appointments():
    search_query = request.args.get('search', '')
    if search_query:
        appointments = Appointment.query.join(Patient).filter(
            Patient.full_name.ilike(f'%{search_query}%')
        ).all()
    else:
        appointments = Appointment.query.all()
    
    return render_template('appointments.html', appointments=appointments, search_query=search_query)

@appointments_bp.route('/appointments/new', methods=['GET', 'POST'])
@login_required
def create_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(reference=form.reference.data).first()
        if not patient:
            flash('Patient not found with the provided reference code.')
            return redirect(url_for('appointments.create_appointment'))
        
        new_appointment = Appointment(
            patient_id=patient.id,
            doctor_id=form.doctor_id.data,
            branch_id=form.branch_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            notes=form.notes.data,
            status='Scheduled'
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        doc = User.query.get_or_404(new_appointment.doctor_id)
        
        patient_email = patient.email 
        subject = "Appointment Confirmation"
        body = f"Dear Patient,\n\nYour appointment is confirmed:\nDoctor: {doc.name}\nDate: {new_appointment.appointment_date}\nTime: {new_appointment.appointment_time}\n\nThank you!"
        send_email(subject, patient_email, body)

        flash('Appointment created and email sent to the patient.')
        return redirect(url_for('appointments.appointments'))
    
    return render_template('appointments/create_appointment.html', form=form)

@appointments_bp.route('/appointments/<int:id>', methods=['GET'])
@login_required
def view_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template('appointments/view_appointment.html', appointment=appointment)

@appointments_bp.route('/appointments/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)

    if form.validate_on_submit():
        patient = Patient.query.filter_by(reference=form.reference.data).first()
        if not patient:
            flash('Patient not found with the provided reference code.')
            return redirect(url_for('appointments.update_appointment', id=id))
        
        appointment.patient_id = patient.id
        appointment.doctor_id = form.doctor_id.data
        appointment.branch_id = form.branch_id.data
        appointment.appointment_date = form.appointment_date.data
        appointment.appointment_time = form.appointment_time.data
        appointment.notes = form.notes.data
        db.session.commit()
        flash('Appointment updated successfully!')
        return redirect(url_for('appointments.appointments'))

    return render_template('appointments/update_appointment.html', form=form, appointment=appointment)

@appointments_bp.route('/appointments/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)

    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the appointment. Please try again.')

    return redirect(url_for('appointments.appointments'))
