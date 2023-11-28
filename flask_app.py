from flask import Flask
from app import app

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    return "INDEX"

if __name__=="__main__":
    app.debug=True
    app.run(debug=True)
