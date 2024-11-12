from flask import Blueprint, render_template, request
from flask_login import login_required
from . import db
from app.models import AuditLog

audits_bp = Blueprint('audits', __name__)

@audits_bp.route('/audits', methods=['GET'])
@login_required
def audits():
    search_query = request.args.get('search', '')
    if search_query:
        # Assuming you want to search by model name or action type in the AuditLog
        audits_data = AuditLog.query.filter(
            (AuditLog.model_name.ilike(f'%{search_query}%')) |
            (AuditLog.action.ilike(f'%{search_query}%'))
        ).all()
    else:
        audits_data = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    
    return render_template('audits.html', audit_logs=audits_data, search_query=search_query)
