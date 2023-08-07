import jwt
import datetime
from app import app

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def verify_token(token):
    try:
        decoded_payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return None  # Token已过期
    except jwt.InvalidTokenError:
        return None  # 无效的Token