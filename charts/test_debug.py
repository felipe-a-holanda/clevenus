from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)


@app.route('/')
def hello_world():
    
    return "<html><body><h1>Hello</h1></body></html>"

if __name__ == '__main__':
    app.run(debug=True)

