import base64
import os
import time

from app import app


def generate_filename(file_extension):
    timestamp_ns = int(time.time_ns())
    return f"{timestamp_ns}{file_extension}"

def save_base64(base64_data,filename):
    try:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        
        # 指定文件路径
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 获取文件的扩展名
        file_extension = os.path.splitext(filename)[1].lower()

        # 最大尝试次数
        max_attempts = 10  
        attempts = 0

        while (os.path.exists(file_path)) and attempts < max_attempts:
            filename = generate_filename(file_extension)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            attempts += 1

        if attempts == max_attempts:
            return None

        file_data = base64.b64decode(base64_data)
        with open(file_path, 'wb') as f:
            f.write(file_data)

        return filename
    except Exception as e:
        print("Error saving file:", e)
        return None