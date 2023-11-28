from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, FloatField, RadioField, SubmitField)
from wtforms.validators import DataRequired, InputRequired, Length

class LoginForm(FlaskForm):
    identifier = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password1 = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Password', validators=[DataRequired()])

class DeleteAccountForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    confirm = StringField('Confirm', validators=[DataRequired()])

