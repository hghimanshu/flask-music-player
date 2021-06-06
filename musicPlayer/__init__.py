from flask import Flask
from flask_bootstrap import Bootstrap
# from flask.ext.session import Session
from musicPlayer.config import config

app = Flask(__name__)
app.config.from_object(__name__)
# Session(app)
Bootstrap(app)

from musicPlayer import routes