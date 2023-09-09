import base64
import datetime
import os
import time

from app import app


def generate_filename(file_extension):
    timestamp_ns = int(time.time_ns())
    return f"{timestamp_ns}{file_extension}"


def create_subfolder(base_folder):
    today = datetime.date.today()
    subfolder_name = today.strftime("%Y-%m-%d")  # 根据日期创建子文件夹名
    subfolder_path = os.path.join(base_folder, subfolder_name)

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    return subfolder_path, subfolder_name


def save_base64(base64_data, filename):
    try:
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])

        # 指定文件路径
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # 获取文件的扩展名
        file_extension = os.path.splitext(filename)[1].lower()

        # 最大尝试次数
        max_attempts = 10
        attempts = 0

        subfolder_path, subfolder_name = create_subfolder(app.config["UPLOAD_FOLDER"])

        while (os.path.exists(file_path)) and attempts < max_attempts:
            filename = generate_filename(file_extension)
            file_path = os.path.join(subfolder_path, filename)
            attempts += 1

        if attempts == max_attempts:
            return None

        file_data = base64.b64decode(base64_data)
        with open(file_path, "wb") as f:
            f.write(file_data)

        return subfolder_name + "/" + filename
    except Exception as e:
        print("Error saving file:", e)
        return None
