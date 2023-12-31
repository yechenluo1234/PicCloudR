import os
from app import app

from flask import send_from_directory, abort

@app.route('/images/<path:subpath>', methods=['GET'])
def get_image(subpath):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], subpath)
    if os.path.exists(image_path):
        if os.path.isdir(image_path):
            abort(404, "图片未找到")
        try:
            # 获取图片的MIME类型
            mime_type = "image/jpeg"  # 默认为JPEG格式
            if subpath.endswith('.png'):
                mime_type = "image/png"

            elif subpath.endswith('.gif'):
                mime_type = "image/gif"

            # 设置Content-Type头信息，不设置Content-Disposition头信息
            response = send_from_directory(app.config['UPLOAD_FOLDER'], subpath)
            response.headers['Content-Type'] = mime_type
            return response
        except Exception as e:
            # 捕获异常并返回适当的错误信息
            return str(e), 500
    else:
        # 返回HTTP 404错误
        abort(404, "图片未找到")

