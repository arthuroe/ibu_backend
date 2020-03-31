from flask import Blueprint

from api.auth.views import LoginView, ManageUserView, UserView

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')
manage_user_view = ManageUserView.as_view('manageuser_api')
auth_blueprint.add_url_rule(
    '/users',
    view_func=manage_user_view,
    methods=['GET', 'POST']
)
auth_blueprint.add_url_rule(
    '/users/<user_id>',
    view_func=manage_user_view,
    methods=['GET', 'DELETE']
)

login_view = LoginView.as_view('login_api')
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

user_view = UserView.as_view('user_api')
auth_blueprint.add_url_rule(
    '/current_user',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/users/<user_id>',
    view_func=user_view,
    methods=['PUT']
)
