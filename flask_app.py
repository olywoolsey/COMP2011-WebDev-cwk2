from app import app

# create a route for the app
# this is the index page
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
