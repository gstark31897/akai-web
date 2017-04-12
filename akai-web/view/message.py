from flask import Blueprint, render_template, g, redirect

from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

import json

from ..model.message import Message

blueprint = Blueprint('message', __name__)


class SendMessageForm(FlaskForm):
    receiver = StringField('Receiver')
    content = TextAreaField('Content')
    submit = SubmitField()
 

@login_required
@blueprint.route('/messages')
def messages():
    messages = Message.get_messages(current_user)
    return render_template('messages.html', messages=messages)


@login_required
@blueprint.route('/send_message', methods=['GET', 'POST'])
def send_message():
    form = SendMessageForm()
    if form.validate_on_submit():
        Message.send_message(form.content.data, current_user, form.receiver.data)
        return redirect('/messages')
    return render_template('login.html', form=form)

