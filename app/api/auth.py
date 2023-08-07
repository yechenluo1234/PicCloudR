from app import app
from flask import request, jsonify

from app.utils.auth import generate_token
    

@app.route('/api/login', methods=['POST'])
def admin_login():
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']
            
            
            if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
                
                token = generate_token(username)
                
                response = {
                    'message': '登录成功',
                    'token': token
                }
                return jsonify(response), 200
            else:
                response = {
                    'message': '登录失败，用户名或密码错误'
                }
                return jsonify(response), 401
                
        except Exception as e:
            print("Error:", e)
            response = {
                'message': '登录失败'
            }
            return jsonify(response), 500
