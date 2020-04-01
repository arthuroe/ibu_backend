from flask import Blueprint

from api.drug.views import DrugView

drug_blueprint = Blueprint('drug', __name__, url_prefix='/api/v1')
drug_view = DrugView.as_view('drug_api')
drug_blueprint.add_url_rule(
    '/drugs',
    view_func=drug_view,
    methods=['GET', 'POST']
)

drug_blueprint.add_url_rule(
    '/drugs/<drug_id>',
    view_func=drug_view,
    methods=['GET', 'PUT', 'DELETE']
)
