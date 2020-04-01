from flask import Blueprint

from api.treatment.views import TreatmentView, TreatmentDrugView

treatment_blueprint = Blueprint('treatment', __name__, url_prefix='/api/v1')
treatment_view = TreatmentView.as_view('treatment_api')
treatment_blueprint.add_url_rule(
    '/treatments',
    view_func=treatment_view,
    methods=['GET', 'POST']
)

treatment_blueprint.add_url_rule(
    '/treatments/<treatment_id>',
    view_func=treatment_view,
    methods=['GET', 'PUT', 'DELETE']
)

treatment_drug_view = TreatmentDrugView.as_view('treatment_drug_api')
treatment_blueprint.add_url_rule(
    '/prescribe/<treatment_id>',
    view_func=treatment_drug_view,
    methods=['POST']
)
