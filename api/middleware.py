from functools import wraps
from flask import jsonify, request
import jwt
from api.model import Usuario

def authenticate_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            username = payload.get('username')
            if not username:
                return jsonify({'error': 'Invalid token'}), 401

            # Fetch user from MongoDB based on the username
            user = Usuario.get_user_by_username(username)
            if not user:
                return jsonify({'error': 'User not found'}), 401

            # Add user information to the request for further processing
            request.user = user

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return func(*args, **kwargs)
    return wrapper

def is_superadmin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.role == 4:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper

def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.role == 3:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper

def is_this_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        client_id = kwargs.get('client_id')  # Assuming client_id is passed in the URL
        if user and user.role == 1 and user.client_id == client_id:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper

def is_tecnico(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.role == 2:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper

def is_sensor_and_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.role == 3 and user.is_sensor:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper

def is_no_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = getattr(request, 'user', None)
        if user and user.role != 1:  # Assuming CLIENTE role is 1
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper

def config_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response