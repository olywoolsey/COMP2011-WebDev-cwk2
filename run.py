from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

# see if user is logged in
def checkuser():
    return True

# landing page
@app.route('/')
def hello_world():
    if checkuser():
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/home')
def home():
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
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

# register page
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.email.data)
        print(form.password1.data)
        print(form.password2.data)
        ## user = User(username=form.username.data,
        ##         email=form.email.data,
        ##         password1=form.password1.data,
        ##         password2=form.password2.data)
        ## print(user)
        ## print(user.username)
        ## print(user.email)
        ## db.session.add(user)
        ## db.session.commit()
        flash('Thanks for registering')
        print('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# run app on local device for testing
if __name__=="__main__":
    app.debug=True
    app.run(debug=True)
