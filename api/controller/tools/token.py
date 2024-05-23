from datetime import datetime, timedelta
import os
import jwt

def generate_token(id_usuario):
    # Generate a token with expiration time
    payload = {
        'id_usuario': id_usuario,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, os.environ.get("SECRET_KEY", "test"), algorithm='HS256')
    return token

def decode_token(token):
    decoded_token = jwt.decode(token, os.environ.get("SECRET_KEY", "test"), algorithms=['HS256'])
    return decoded_token

def generate_token_by_user(user):
    return generate_token(user['id_usuario'])

def verify_token(token):
    try:
        result = jwt.decode(token, os.environ.get("SECRET_KEY", "test"), algorithms=['HS256'])
        return result
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None