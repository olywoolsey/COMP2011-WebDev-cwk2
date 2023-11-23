from app import app

@app.route('/')
def Welcome():
    return "Welcome to Flask App!"

# Starts the app
if __name__=="__main__":
    app.debug=True
    app.run(debug=True)
