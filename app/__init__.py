from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('../config/config.py')

from app.api import upload, retrieve , auth
