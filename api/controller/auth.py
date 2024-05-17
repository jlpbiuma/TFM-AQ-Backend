from flask import jsonify, request
from api.model import Usuario
import jwt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import hashlib


def generate_token(username):
    # Generate a token with expiration time
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, os.environ.get("SECRET_KEY", "test"), algorithm='HS256')
    return token

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    rol = data.get('rol')  # Assuming rol is also provided in the request

    if not username or not email or not name or not password or not rol:
        return jsonify({'error': 'Username, email, name, password, and rol are required'}), 400

    # Check if username or email is already in use
    if Usuario.get_user_by_username(username):
        return jsonify({'error': 'Username is already in use'}), 400
    if Usuario.get_user_by_email(email):
        return jsonify({'error': 'Email is already in use'}), 400

    user = Usuario(username, email, name, password, rol)
    user.save()

    # Generate token
    token = generate_token(username)

    return jsonify({'token': token }), 201

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
        token = generate_token(username)
        return jsonify({'token': token }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    return send_password_reset_email(email)

def send_password_reset_email(target_email):
    # Generate token
    user = Usuario.get_user_by_email(target_email)
    if user:
        token = generate_token(target_email)  # Use email as a unique identifier for the token

        # Send email
        sender_email = os.environ.get('EMAIL_BOT')  # Update with your email address
        password = os.environ.get('EMAIL_PASSWORD_TFM')  # Update with your email password
        smtp_server = os.environ.get('EMAIL_SERVER')  # Update with your SMTP server address
        smtp_port = int(os.environ.get('EMAIL_PORT'))  # Update with your SMTP server port

        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset Request"
        message["From"] = sender_email
        message["To"] = target_email

        # Create the HTML content of the email
        html = f"""
        <html>
            <body>
                <p>Hello,</p>
                <p>You requested a password reset for your account.</p>
                <p>Please click the link below to reset your password:</p>
                <p><a href="http://your_website.com/auth/reset_password?token={token}">Reset Password</a></p>
                <p>If you didn't request a password reset, you can safely ignore this email.</p>
            </body>
        </html>
        """

        # Attach HTML content to the email
        message.attach(MIMEText(html, "html"))

        # Connect to SMTP server and send email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, target_email, message.as_string())
                return jsonify({"message": "Password reset email sent"}), 200
            except smtplib.SMTPAuthenticationError:
                # Failed to login due to incorrect credentials
                return jsonify({"error": "Failed to login with provided email credentials"}), 401
            except Exception as e:
                # Other exceptions (e.g., network issues)
                return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "User not found"}), 404

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
        decoded_token = jwt.decode(token, os.environ.get("SECRET_KEY", "test"), algorithms=['HS256'])
        token_email = decoded_token.get('username')  # We used email as the username in the token

        # Verify the token email matches the provided email
        if token_email != email:
            return jsonify({"error": "Invalid token for the provided email"}), 401

        # Hash the new password
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

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