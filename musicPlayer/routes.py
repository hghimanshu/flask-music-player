from musicPlayer import app
import json
import sys
from werkzeug import secure_filename
import flask
import time


@app.route('/home')
def home():
    return '<h2>Heelo</h2>'
