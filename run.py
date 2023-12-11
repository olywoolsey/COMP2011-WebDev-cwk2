from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, case, join
from flask_restful import Resource, Api
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from forms import LoginForm, RegistrationForm, DeleteAccountForm, NewEventForm, NewFriendForm, RemoveFriendForm, AcceptFriendForm, RejectFriendForm, CancelFriendForm
# from forms import *

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
    accepted = db.Column(db.Integer) # 0 = not accepted, 1 = accepted

# see if user is logged in
def checkUser():
    if session.get('logged_in'):
        return True
    else:
        return False

# landing page
@app.route('/')
def index():
    if checkUser():
        return redirect(url_for('home'))
    else:
        return render_template('index.html')

@app.route('/home')
def home():
    if checkUser():
        username = User.query.filter_by(id=session['userID']).first().username
        picture = './static/uploads/' + username + '.jpg'
        events = Event.query.filter_by(user_id=session['userID']).all()
        invitations = EventFriend.query.filter_by(friend_id=session['userID']).all()
        eventInvitations = []
        for i in invitations:
            eventInvitations.append(Event.query.filter_by(id=i.event_id).first())
        return render_template('home.html', profile_picture=picture, username=username, events=events, eventInvitations=eventInvitations)
    else:
        return render_template('index.html')

# login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.identifier.data).first()
        if user is None:
            user = User.query.filter_by(email=form.identifier.data).first()
        if user is None:
            flash('Invalid username or email')
            return redirect(url_for('login'))
        if user.password != form.password.data:
            flash('Invalid password')
            return redirect(url_for('login'))
        flash('Logged in successfully')
        # Add the user to the session to keep them logged in
        session['logged_in'] = True
        session['userID'] = user.id
        session.permanent = True
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

# register page
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password1.data != form.password2.data:
            flash('Passwords do not match')
            return redirect(url_for('register'))
        elif User.query.filter_by(username=form.username.data).first() is not None:
            flash('Username already exists')
            return redirect(url_for('register'))
        elif User.query.filter_by(email=form.email.data).first() is not None:
            flash('Email already exists')
            return redirect(url_for('register'))
        else:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password2.data)
            db.session.add(user)
            db.session.commit()
            session['logged_in'] = True
            session['userID'] = User.query.filter_by(username=form.username.data).first().id
            session.permanent = True
            return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    # Clear the session data
    session["logged_in"] = False
    # Redirect to the home page or any other desired page
    return redirect(url_for('home'))

@app.route('/delete_account', methods=('GET', 'POST'))
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        username = User.query.filter_by(id=session['userID']).first().username
        user = User.query.filter_by(username=username).first()
        if form.password.data != form.confirm.data:
            flash('Passwords do not match')
        elif user.password != form.password.data:
            flash('Invalid password')
        elif user.password == form.password.data:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('logout'))
        return redirect(url_for('delete_account'))
    return render_template('delete_account.html', form=form)

@app.route('/change_profile_picture', methods=('GET', 'POST'))
def change_profile_picture():
    if checkUser():
        if request.method == 'POST':
            f = request.files['profile_picture']
            username = User.query.filter_by(id=session['userID']).first().username
            filename = secure_filename(username + '.jpg')
            f.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    return "Profile Picture Changed"

@app.route('/create_event', methods=('GET', 'POST'))
def create_event(): 
    form = NewEventForm()
    if checkUser():
        # must add friends to form before validating so that form.guests.choices is populated
        friendship = Friend.query.filter(((Friend.user_id1 == session['userID']) | (Friend.user_id2 == session['userID'])) & (Friend.status == 1)).all()
        friendsList = []
        for i in friendship:
            if i.user_id1 == session['userID']:
                friendsList.append(User.query.filter_by(id=i.user_id2).first())
            else:
                friendsList.append(User.query.filter_by(id=i.user_id1).first())
        # add friends to form
        form.guests.choices = [(str(i.id), i.username) for i in friendsList]
        if form.validate_on_submit():
            guests = form.guests.data
            newEvent = Event(name=form.name.data,
                             description=form.description.data,
                             location=form.location.data,
                             date=form.datetime.data,
                             time=form.datetime.data,
                             user_id=session['userID'])
            db.session.add(newEvent)
            db.session.commit()
            eventId = newEvent.id
            for i in guests:
                eventFriend = EventFriend(event_id=eventId,
                                friend_id=i, accepted=0)
                db.session.add(eventFriend)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print(form.errors)
        return render_template('create_event.html', form=form, friendsList=friendsList)
    else:
        return render_template('index.html')

@app.route('/event/<eventId>', methods=('GET', 'POST'))
def event(eventId):
    if checkUser():
        event = Event.query.filter_by(id=eventId).first()
        eventFriends = EventFriend.query.filter_by(event_id=eventId).all()
        guests = []
        for i in eventFriends:
            guests.append(User.query.filter_by(id=i.friend_id).first())
        print(guests)
        return render_template('event.html', event=event, guests=guests)
    else:
        return render_template('index.html')

@app.route('/friends', methods=('GET', 'POST'))
def friends():
    formNew = NewFriendForm()
    formRemove = RemoveFriendForm()
    formAccept = AcceptFriendForm()
    formReject = RejectFriendForm()
    formCancel = CancelFriendForm()
    if checkUser():
        if formNew.validate_on_submit():
            if User.query.filter_by(username=formNew.username.data).first() is None:
                flash('User does not exist')
            elif User.query.filter_by(username=formNew.username.data).first().id == session['userID']:
                flash('Cannot add yourself')
            elif Friend.query.filter_by(user_id1=session['userID'], user_id2=User.query.filter_by(username=formNew.username.data).first().id).first() is not None:
                flash('Friend already added')
            elif Friend.query.filter_by(user_id2=session['userID'], user_id1=User.query.filter_by(username=formNew.username.data).first().id).first() is not None:
                flash('Friend already added')
            else:
                id1 = session['userID']
                id2 = User.query.filter_by(username=formNew.username.data).first().id
                friend = Friend(user_id1=id1, user_id2=id2, status=0)
                db.session.add(friend)
                db.session.commit()
        elif formRemove.validate_on_submit():
            try:
                friends = Friend.query.filter_by(user_id1=session['userID'], user_id2=formRemove.remove_friend_id.data).first()
                db.session.delete(friends)
            except:
                friends = Friend.query.filter_by(user_id2=session['userID'], user_id1=formRemove.remove_friend_id.data).first()
                db.session.delete(friends)
            db.session.commit()
        elif formAccept.validate_on_submit():
            friendship = Friend.query.filter_by(user_id2=session['userID'], user_id1=formAccept.accept_friend_id.data).first()
            friendship.status = 1
            db.session.commit()
        elif formReject.validate_on_submit():
            try:
                friends = Friend.query.filter_by(user_id1=session['userID'], user_id2=formReject.reject_friend_id.data).first()
                db.session.delete(friends)
            except:
                friends = Friend.query.filter_by(user_id2=session['userID'], user_id1=formReject.reject_friend_id.data).first()
                db.session.delete(friends)
            db.session.commit()
        elif formCancel.validate_on_submit():
            try:
                friends = Friend.query.filter_by(user_id1=session['userID'], user_id2=formCancel.cancel_friend_id.data).first()
                db.session.delete(friends)
            except:
                friends = Friend.query.filter_by(user_id2=session['userID'], user_id1=formCancel.cancel_friend_id.data).first()
                db.session.delete(friends)
            db.session.commit()
        friends = Friend.query.filter(
            or_(Friend.user_id1 == session['userID'], Friend.user_id2 == session['userID'])
        ).all()
        friendsList = []
        friendsRequestRecieved = []
        friendsRequestSent = []
        for i in friends:
            if i.status == 1:
                if i.user_id1 == session['userID']:
                    friendsList.append(User.query.filter_by(id=i.user_id2).first())
                else:
                    friendsList.append(User.query.filter_by(id=i.user_id1).first())
            elif i.status == 0:
                if i.user_id1 == session['userID']:
                    friendsRequestSent.append(User.query.filter_by(id=i.user_id2).first())
                else:
                    friendsRequestRecieved.append(User.query.filter_by(id=i.user_id1).first())
        return render_template('friends.html',
                               username=User.query.filter_by(id=session['userID']).first().username,
                               formNew=formNew,
                               formRemove=formRemove,
                               formAccept=formAccept,
                               formReject=formReject,
                               formCancel=formCancel,
                               friendsList=friendsList,
                               friendsRequestSent=friendsRequestSent,
                               friendsRequestRecieved=friendsRequestRecieved)
    else:
        return redirect(url_for('home'))

@app.route('/settings', methods=('GET', 'POST'))
def settings():
    if checkUser():
        return render_template('settings.html')
    else:
        return render_template('index.html')

@app.route('/calendar_data', methods=('GET', 'POST'))
def calendar_data():
    if checkUser():
        events = Event.query.filter_by(user_id=session['userID']).all()
        data = []
        for i in events:
            data.append({'name': i.name, 'date': i.date, 'id' : str(i.id)})
        print(events)
        print(data)
        return data
    else:
        return render_template('index.html')

# run app on local device for testing
if __name__=="__main__":
    app.debug=True
    app.run(debug=True)
