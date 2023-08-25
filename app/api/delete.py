from app import app
from flask import request, jsonify

from app.utils.auth import verify_token
from app.utils.delete import delete_old_files


@app.route('/api/deleteOldFiles', methods=['POST'])
def delete_old_files_api():
    try:

        # 验证token
        token = request.headers.get('Authorization')
        if not token:
            response = {
                "message": "缺少认证Token"
            }
            return jsonify(response), 401

        # 分割 Authorization 头部，获取实际的 token 部分
        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            response = {
                "message": "Token格式不正确"
            }
            return jsonify(response), 401

        # 获取实际的 token
        actual_token = token_parts[1]

        decoded_payload = verify_token(actual_token)
        if not decoded_payload or decoded_payload['username'] != app.config['ADMIN_USERNAME']:
            response = {
                "message": "Token无效或与用户不匹配"
            }
            return jsonify(response), 401



        data = request.get_json()
        days = data['days']
        delete_old_files(days)
        response = {
            'message': '删除成功'
        }
        return jsonify(response), 200
    except Exception as e:
        print("Error:", e)
        response = {
            'message': '删除失败'
        }
        return jsonify(response), 500