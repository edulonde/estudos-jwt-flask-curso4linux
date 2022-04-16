import flask
from dotenv import load_dotenv
from api.auth import blueprint as auth
from frontend.views import blueprint as views
from api.profile import blueprint as profile

load_dotenv()

app = flask.Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(views)
app.register_blueprint(profile)

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/login")
def login():
    return flask.render_template('login.html')


@app.route("/profile")
def profile():
    return flask.render_template('profile.html')
