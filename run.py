import logging
from waitress import serve
from app import app

logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

serve(app, host="0.0.0.0", port=app.config["PORT"])


app.logger.info("exiting Done")
