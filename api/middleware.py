from functools import wraps
from flask import jsonify, request, g
from api.model import Usuario, Logs
from functools import wraps
from api.controller.tools import *

# Middleware to check if the user is a superadmin (role 4)
def is_superadmin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get role and id_usuario by request
        token = request.headers.get('Authorization')
        role = Usuario.get_role_by_token(token)
        if role == 4:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Recurso no accesible"})
    return wrapper

# Middleware to check if the user is an admin (role 3)
def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get role and id_usuario by request
        token = request.headers.get('Authorization')
        role = Usuario.get_role_by_token(token)
        if role >= 3:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Recurso no accesible"})
    return wrapper

# Middleware to check if the user is a tecnico (role 2)
def is_tecnico(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get role and id_usuario by request
        token = request.headers.get('Authorization')
        role = Usuario.get_role_by_token(token)
        if role >= 2:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Recurso no accesible"})
    return wrapper

# Middleware to check if the user is a tecnico (role 2)
def is_this_client_usuario(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify token presence
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token necesario'})

        # Verify token validity
        if not verify_token(token):
            return jsonify({'error': 'Token expirado'})

        # Verify user ID presence
        requested_id_usuario = kwargs.get('id_usuario')
        if not requested_id_usuario:
            return jsonify({'error': 'No se especifica el usuario del que se quiere pedir la informacion'})

        # Check user role
        role = Usuario.get_role_by_id(requested_id_usuario)
        if role >= 2:
            return func(*args, **kwargs)

        # Allow access if the action is about their own data and they have role 1
        id_usuario = request.get_json().get('sesion_id_usuario')
        if not id_usuario:
            return jsonify({'error': 'No se especifica el usuario de la sesión actual'})
        if role == 1 and requested_id_usuario == id_usuario:
            return func(*args, **kwargs)

        return jsonify({"error": "Recurso no accesible"})
    return wrapper

# Define other middleware functions similarly...
def config_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

def log_request():
    g.request_data = {
        "endpoint": request.path,
        "method": request.method,
        "ip_address": request.remote_addr,
        "timestamp": datetime.utcnow(),
        "request_body": request.get_data(as_text=True)
    }

def log_response(response):
    response_data = {
        "status_code": response.status_code,
        "response_body": response.get_data(as_text=True)
    }

    log_data = {**g.request_data, **response_data}
    save_log(log_data)
    return response

def save_log(log_data):
    new_log = Logs(
        ENDPOINT=log_data["endpoint"],
        METHOD=log_data["method"],
        STATUS_CODE=log_data["status_code"],
        IP_ADDRESS=log_data["ip_address"],
        TIMESTAMP=log_data["timestamp"],
        REQUEST_BODY="",
        RESPONSE_BODY=""
    )
    new_log.save()
    return new_log