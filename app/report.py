from flask import render_template, make_response, Blueprint
import pdfkit
from app.models import Patient, MedicalHistory


report_bp = Blueprint('reports', __name__)


path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)


@report_bp.route('/generate_pdf/<int:id>', methods=['GET'])
def generate_pdf(id):
    patient = Patient.query.get_or_404(id)
    medicals = MedicalHistory.query.filter_by(patient_id=id).all()
    html = render_template('pdf_template.html', patient=patient, medicals=medicals)
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response