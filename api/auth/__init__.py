from flask import Blueprint

from api.auth.views import LoginView

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')
login_view = LoginView.as_view('login_api')
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
