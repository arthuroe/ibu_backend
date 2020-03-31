import os

from flask import Flask
from flask_cors import CORS
import flask_excel as excel

from config import app_configuration

app = Flask(__name__)

environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])

from api.models import db
from api.auth import auth_blueprint
from api.export import export_blueprint
from api.users import user_blueprint

db.init_app(app)
excel.init_excel(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(export_blueprint)
app.register_blueprint(user_blueprint)

# add support for CORS for all end points
CORS(app)


@app.route('/')
def index():
    return "Welcome to IBU API"
