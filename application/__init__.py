from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
appDB = SQLAlchemy(app)
login_manager = LoginManager(app)
mail_manager = Mail(app)


from application.views import index, workshops, signin, users, logout, type_and_time, workshop_activity, error
