import os
from flask import request, jsonify
from app import app

from app.utils.auth import verify_token
from app.utils.upload import save_base64



@app.route('/api/uploadByBase64', methods=['POST'])
def upload_from_base64():
    try:
        data = request.get_json()
        image_base64 = data['imageBase64']
        filename = data['filename']

        # 验证文件格式
        file_extension = os.path.splitext(filename)[1].lower()
        if((file_extension!='.jpg') & (file_extension != '.png') & (file_extension != '.gif')):
            response = {
                "message": "图片格式不正确"
            }
            return jsonify(response), 500



        # 验证token
        token = request.headers.get('Authorization')
        if not token:
            response = {
                "message": "缺少认证Token"
            }
            return jsonify(response), 401
        
        decoded_payload = verify_token(token)
        if not decoded_payload or decoded_payload['username'] != app.config['ADMIN_USERNAME']:
            response = {
                "message": "Token无效或与用户不匹配"
            }
            return jsonify(response), 401
        




        # 保存图片
        filename = save_base64(image_base64,filename)
        if filename:
            response = {
                "message": "图片上传成功",
                "file_url": f"/images/{filename}"
            }
            return jsonify(response), 200
        else:
            response = {
                "message": "图片上传失败"
            }
            return jsonify(response), 500
        


    except Exception as e:
        print("Error:", e)
        response = {
            "message": "图片上传失败"
        }
        return jsonify(response), 500
