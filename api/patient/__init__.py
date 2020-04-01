from flask import Blueprint

from api.patient.views import PatientView

patient_blueprint = Blueprint('patient', __name__, url_prefix='/api/v1')
patient_view = PatientView.as_view('patient_api')
patient_blueprint.add_url_rule(
    '/patients',
    view_func=patient_view,
    methods=['GET', 'POST']
)

patient_blueprint.add_url_rule(
    '/patients/<patient_id>',
    view_func=patient_view,
    methods=['GET', 'PUT', 'DELETE']
)
