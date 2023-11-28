from flask import Flask
from flask import Flask, render_template, redirect, url_for, flash, request

app = Flask(__name__)
app.config.from_object('config')

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

# login page
@app.route('/login')
def login():
    return render_template('login.html')

# run app on local device for testing
if __name__=="__main__":
    app.debug=True
    app.run(debug=True)
