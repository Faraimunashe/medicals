from flask import Blueprint, render_template
from flask_login import login_required
from . import db
from app.models import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
