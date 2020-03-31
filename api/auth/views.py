import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api.auth.helpers import *
from api.decorators import token_required
from api.models import User


class LoginView(MethodView):
    """
    View to login the user
    """

    def post(self):
        try:
            post_data = request.json
            email = post_data.get('email')
            password = post_data.get('password')

            if not email or not password:
                response = {
                    'status': 'fail',
                    'message': 'email or password not provided.'
                }
                return make_response(jsonify(response)), 400

            if not validate_email(email):
                response = {
                    'status': 'fail',
                    'message': 'Invalid email or password provided'
                }
                return make_response(jsonify(response)), 400

            user = User.find_first(email=email)

            if user and not user.password_is_valid(password):
                response = {
                    'status': 'fail',
                    'message': 'Invalid email or password provided'
                }
                return make_response(jsonify(response)), 401

            if user and user.password_is_valid(password):
                auth_token = user.generate_token(user.id)
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'An error has occurred. Please try again.'
            }
            return make_response(jsonify(response)), 500


class ManageUserView(MethodView):
    """
    View to manage user accounts
    """
    decorators = [token_required]

    def get(self, current_user, user_id=None):
        try:
            if user_id:
                user = User.find_first(id=user_id)
                if not user:
                    response = {
                        'status': 'fail',
                        'message': 'User does not exist'
                    }
                    return make_response(jsonify(response)), 400

                response = {
                    'status': 'success',
                    'user': user.serialize()
                }
                return make_response(jsonify(response)), 200

            users = User.fetch_all()

            if not users:
                response = {
                    'status': 'success',
                    'message': 'No users have been added'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'success',
                'users': [user.serialize() for user in users]
            }
            return make_response(jsonify(response)), 200

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to retrieve users.'
            }
            return make_response(jsonify(response)), 400

    def post(self, current_user):
        post_data = request.json
        email = post_data.get('email')
        name = post_data.get('name')
        password = post_data.get('password')

        if not all([email, name, password]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. email, name and '
                            'password must be provided')
            }
            return make_response(jsonify(response)), 400

        user = User.find_first(email=post_data.get('email'))
        if not user:
            try:
                user = User(email=email, password=password, name=name)
                user.save()

                response = {
                    'status': 'success',
                    'message': f'Successfully Added {user.name}.'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                logging.error(f"An error has occurred  {e}")
                response = {
                    'status': 'fail',
                    'message': 'Registration failed. Please try again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists.',
            }
            return make_response(jsonify(response)), 409

    def delete(self, current_user, user_id):
        try:
            user = User.find_first(id=user_id)
            if user:
                user.delete()
                response = {
                    'status': 'success',
                    'message': f'Successfully deleted {user.name}.'
                }
                return make_response(jsonify(response)), 200

            response = {
                'status': 'fail',
                'message': 'User does not exist.',
            }
            return make_response(jsonify(response)), 400

        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Delete failed. Please try again.'
            }
            return make_response(jsonify(response)), 401


class UserView(MethodView):
    """
    View to enable users view and update their details
    """
    decorators = [token_required]

    def get(self, current_user):
        user_id = current_user.id

        try:
            user = User.find_first(id=user_id)

            if not user:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 400

            user = {
                "email": user.email,
                "id": user.id,
                "is_admin": user.is_admin,
                "name": user.name,
                "photo": user.photo,
            }
            response = {
                'status': 'success',
                'user': user
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to retrieve user.'
            }
            return make_response(jsonify(response)), 400

    def put(self, current_user, user_id):
        kwargs = request.json
        try:
            user = User.find_first(id=user_id)
            if user:
                user = User(**kwargs)
                user.save()

                response = {
                    'status': 'success',
                    'message': f'Successfully updated {user.name}.'
                }
                return make_response(jsonify(response)), 201

            response = {
                'status': 'fail',
                'message': 'User does not exist.',
            }
            return make_response(jsonify(response)), 400
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Update failed. Please try again.'
            }
            return make_response(jsonify(response)), 401
