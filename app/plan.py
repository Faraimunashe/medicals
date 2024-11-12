from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from . import db
from app.models import Patient, MedicalHistory
from app.audit_helper import log_update

plan_bp = Blueprint('plans', __name__)

@plan_bp.route('/plans', methods=['GET', 'POST'])
@login_required
def plans():
    search_query = request.args.get('search', '')
    if search_query:
        patient = Patient.query.filter_by(reference=search_query).first()
        if patient:
            search_query = patient.id
        medicals = MedicalHistory.query.filter(
            (MedicalHistory.patient_id.ilike(f'%{search_query}%'))
        ).all()
    else:
        medicals = MedicalHistory.query.all()
        
    return render_template('plans.html', medicals=medicals, search_query=search_query)



@plan_bp.route('/plan/new', methods=['POST'])
def create_plan():
    data = request.get_json()
    #print(data)
    
    mid = data.get('medical_id')
    plan = data.get('plan')
    if not all([mid, plan]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    medical = MedicalHistory.query.filter_by(id=mid).first()
    #print(mid)
    #print(medical)
    if not medical:
        return jsonify({'message': 'Missing medical record'}), 400
    
    medical_old = medical.to_dict()
    medical.plan = plan
    db.session.commit()
        
    log_update(medical, medical_old)
    return jsonify({'message': 'Plan has been update successfully'}), 200

