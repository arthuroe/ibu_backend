import jwt
import logging

from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

from api import app
from api.models import db, ModelMixin


class User(ModelMixin):
    """
    User model attributes
    """
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(180))
    role = db.Column(db.String(180), default="Doctor")

    def __init__(self, email=None, password=None, name=None):
        """
        Initializes the user instance
        """
        self.email = email
        self.password = self.hash_password(password)
        self.name = name

    def hash_password(self, password):
        if password:
            return Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Check the password against its hash to validate it
        """
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user):
        """
        Generate access token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=12),
                'iat': datetime.utcnow(),
                'sub': user
            }
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            logging.error(f"An error while generating a token {e}")
            return str(e)

    @staticmethod
    def decode_token(token):
        """
        Decodes the access token from the Authorization header.
        """
        try:
            payload = jwt.decode(
                token, app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
