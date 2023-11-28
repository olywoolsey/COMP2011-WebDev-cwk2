from flask import Flask

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
