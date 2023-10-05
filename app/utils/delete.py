import os
import shutil

from termcolor import colored
from app import app
import datetime

directory_path = app.config['UPLOAD_FOLDER']


def delete_old_files(days):
    current_date = datetime.datetime.now()
    three_days_ago = current_date - datetime.timedelta(days=days)

    for filename in os.listdir(directory_path):
        try:
            file_date = datetime.datetime.strptime(filename, '%Y-%m-%d')
            if file_date < three_days_ago:
                file_path = os.path.join(directory_path, filename)
                shutil.rmtree(file_path)
                colored_filename = colored(filename, 'yellow')
                app.logger.info(f"Deleted file: {colored_filename}")
        except ValueError:
            continue
