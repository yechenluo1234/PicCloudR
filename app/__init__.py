import logging
import os
from flask import Flask

app = Flask(__name__)

logging.basicConfig(format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s', level=logging.INFO)

if(os.path.exists("./config/dev_config.py")):
    app.config.from_pyfile('../config/dev_config.py')
    app.debug=True
else:
    app.config.from_pyfile('../config/config.py')

from app.api import upload, retrieve, auth
