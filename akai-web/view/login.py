import flask
from flask import Blueprint, render_template, g

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from flask_login import login_required, login_user

from ..model.user import User
from .. import login_manager

blueprint = Blueprint('login', __name__)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()


login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(username):
    print('getting user: {}'.format(username))
    return User.get_user(username)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.username.data)
        user.login(form.password.data)

        login_user(user)
        next = flask.request.args.get('next')

        return flask.redirect(next or '/')
    return render_template('login.html', form=form)


@blueprint.route('/stuff')
@login_required
def stuff():
    return 'secret stuff'
