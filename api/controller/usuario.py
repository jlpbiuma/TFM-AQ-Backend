# user_controller.py
from flask import jsonify, request
from api.model import Usuario

def create_usuario():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    rol = data.get('rol')  # Assuming rol is also provided in the request

    if not username or not email or not name or not password:
        return jsonify({'error': 'Username, email, name, and password are required'}), 400

    user = Usuario(username, email, name, password, rol)
    user = user.save()
    return jsonify(user), 201

def get_usuario(id_usuario):
    user = Usuario.get_user_by_id(id_usuario)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

def get_usuario_list():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    users = Usuario.get_users_by_pagination(page, per_page)
    return jsonify(users), 200

def update_usuario(id_usuario):
    data = request.get_json()
    user = Usuario.get_user_by_id(id_usuario)
    if user:
        user = Usuario.update_user_by_id(id_usuario, data)
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

def delete_usuario(id_usuario):
    user = Usuario.get_user_by_id(id_usuario)
    if user:
        user = Usuario.delete_user_by_id(id_usuario)
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404
