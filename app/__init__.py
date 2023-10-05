import logging
import os
from flask import Flask, request
from termcolor import colored


app = Flask(__name__)


logging.basicConfig(
    format="[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s", level=logging.INFO
)


# 开启DEBUG模式时在每次请求之后记录请求信息
@app.after_request
def log_response_info(response):
    if app.config["DEBUG"]:
        colored_request_method_info = colored(request.method, "yellow")
        colored_response_status_info = colored(response.status, "yellow")
        app.logger.info(
            "%s %s - %s ",
            colored_request_method_info,
            request.url,
            colored_response_status_info,
        )
    return response


if os.path.exists("./config/dev_config.py"):
    app.config.from_pyfile("../config/dev_config.py")
else:
    app.config.from_pyfile("../config/config.py")

with open("banner.txt", "r") as file:
    content = file.read()
    print(colored(content, "yellow"))

app.logger.info("Initialization complete")

if app.config["DEBUG"]:
    app.logger.info("Running in DEBUG mode")


from app.api import upload, retrieve, auth, delete
