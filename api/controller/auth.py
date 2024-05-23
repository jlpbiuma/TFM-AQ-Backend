from flask import jsonify, request
from api.model import Usuario
from api.controller.tools import *

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    rol = 1

    if not username or not email or not name or not password:
        return jsonify({'error': 'Username, email, name, password are required'}), 400

    # Check if username or email is already in use
    if Usuario.get_user_by_username(username):
        return jsonify({'error': 'Username is already in use'}), 400
    if Usuario.get_user_by_email(email):
        return jsonify({'error': 'Email is already in use'}), 400

    user = Usuario(username, email, name, password, rol)
    user = user.save()
    # Generate token
    token = generate_token_by_user(user)
    rol = get_rol_by_user(user)
    id_usuario = get_id_usuario_by_user(user)
    return jsonify({'token': token, 'role': rol, 'id_usuario': id_usuario}), 201

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Example authentication logic
    user = Usuario.authenticate(username, password)
    if user:
        # Generate and return a token
        token = generate_token_by_user(user)
        rol = get_rol_by_user(user)
        id_usuario = get_id_usuario_by_user(user)
        return jsonify({'token': token, 'role': rol, 'id_usuario': id_usuario}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400
    user = Usuario.get_user_by_email(email)
    if user:
        result_message, result_code = send_password_reset_email(email)
    else:
        return jsonify({'error': 'Email not found'}), 404
    return jsonify(result_message), result_code

def reset_password():
    # Get data from the request
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    token = data.get('token')

    # Check if email and new_password are provided
    if not email or not new_password:
        return jsonify({"error": "Email and new password are required"}), 400

    try:
        # Decode the token to get the email
        decoded_token = decode_token(token)
        token_email = decoded_token.get('username')  # We used email as the username in the token

        # Verify the token email matches the provided email
        if token_email != email:
            return jsonify({"error": "Invalid token for the provided email"}), 401

        # Hash the new password
        hashed_password = hashed_password(new_password)

        # Update the user's password in the database
        user = Usuario.get_user_by_email(email)
        if user:
            user['password'] = hashed_password
            Usuario.update_user_by_id(user['_id'], user)
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401