from flask import Blueprint, render_template
from flask_login import login_required
from . import db
from app.models import Patient

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    return render_template('patients.html')