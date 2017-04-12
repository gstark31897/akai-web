from flask import  Flask, render_template
from flask_login import LoginManager

from flask_bootstrap import Bootstrap

import os

from mongoengine import *

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# app
app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

# db
connect('akai')

# views
from .view import login
app.register_blueprint(login.blueprint)


@app.route('/')
def index():
    return 'Hello World'

