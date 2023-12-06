from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(120), index=True, unique=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(120))
    location = db.Column(db.String(120))
    date = db.Column(db.String(120))
    time = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer)

class EventFriend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))

