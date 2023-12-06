from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, FloatField, RadioField, SubmitField, DateField, SelectField, SelectMultipleField)
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

class NewEventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    location = StringField('Location')
    datetime = DateField('Date', validators=[DataRequired()])
    # people has to be a drop down list of people
    guests = SelectMultipleField('Guests')

class NewFriendForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

class AcceptFriendForm(FlaskForm):
    accept_friend_id = IntegerField('ID', validators=[DataRequired()])

class RejectFriendForm(FlaskForm):
    reject_friend_id = IntegerField('ID', validators=[DataRequired()])

class RemoveFriendForm(FlaskForm):
    remove_friend_id = IntegerField('ID', validators=[DataRequired()])

class CancelFriendForm(FlaskForm):
    cancel_friend_id = IntegerField('ID', validators=[DataRequired()])
