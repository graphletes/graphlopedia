from flask import Flask
import flask_login

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('GRAPH_SETTINGS')

import graph.views
from graph.utilities import User

lm = flask_login.LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def user_loader(email):
	u = User.get(email)
	return u