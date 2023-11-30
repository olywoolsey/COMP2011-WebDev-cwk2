from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from forms import LoginForm, RegistrationForm, DeleteAccountForm

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

# see if user is logged in
def checkUser():
    if session.get('logged_in'):
        return True
    else:
        return False

# landing page
@app.route('/')
def hello_world():
    if checkUser():
        return redirect(url_for('home'))
    else:
        return render_template('index.html')

@app.route('/home')
def home():
    if checkUser():
        picture = './static/uploads/' + session['username'] + '.jpg'
        return render_template('home.html', profile_picture=picture)
    else:
        return render_template('index.html')

# login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.identifier.data)
        print(form.password.data)
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
        session['username'] = user.username
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
            session['username'] = user.username
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
        username = session['username']
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
            filename = secure_filename(session['username'] + '.jpg')
            # delete old profile picture
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Profile Picture Changed"

# run app on local device for testing
if __name__=="__main__":
    app.debug=True
    app.run(debug=True)
