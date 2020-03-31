from flask import Blueprint

from api.export.views import ExportView


export_blueprint = Blueprint('export', __name__, url_prefix='/api/v1')
export_blueprint.add_url_rule(
    '/export',
    view_func=ExportView.as_view('export_api'),
    methods=['GET']
)
