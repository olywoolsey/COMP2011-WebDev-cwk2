from flask_wtf import FlaskForm
from wtforms import (validators, StringField, PasswordField, TextAreaField, IntegerField, BooleanField, FloatField, RadioField, SubmitField, DateField, SelectField, SelectMultipleField, widgets, HiddenField, ValidationError)
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    identifier = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()]) # TODO: Add email validator , Email(message='Invalid email address')
    password1 = PasswordField('Password', validators=[DataRequired(),
                                                      Length(min=8, message="Password must be at least 8 characters long"),
                                                      EqualTo('password2', message='Passwords must match')
                                                      ])
    password2 = PasswordField('Password', validators=[DataRequired(),
                                                      Length(min=8, message="Password must be at least 8 characters long"),
                                                      EqualTo('password1', message='Passwords must match')
                                                      ])

class DeleteAccountForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    confirm = StringField('Confirm', validators=[DataRequired()])

class NewEventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    location = StringField('Location')
    datetime = DateField('Date', validators=[DataRequired()])
    guests = SelectMultipleField('Guests', choices=[], widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())

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

class AcceptEventForm(FlaskForm):
    accept_event_id = IntegerField('ID', validators=[DataRequired()])
