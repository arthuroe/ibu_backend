import os

from flask import Flask
from flask_cors import CORS

from config import app_configuration

app = Flask(__name__)

environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])

from api.models import db
from api.auth import auth_blueprint

db.init_app(app)

app.register_blueprint(auth_blueprint)

# add support for CORS for all end points
CORS(app)


@app.route('/')
def index():
    return "Welcome to IBU API"
