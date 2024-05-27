from flask_mail import Message
from api.controller.tools import generate_token
from flask import current_app
from api.mail import mail

def send_password_reset_email(target_email):
    # Generate token
    token = generate_token(target_email)

    # Create the plain text and HTML parts of the email
    text = f"""
    Hello,

    You requested a password reset for your account.

    Please click the link below to reset your password:
    http://your_website.com/auth/reset_password?token={token}

    If you didn't request a password reset, you can safely ignore this email.
    """

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

    # Create message
    msg = Message(subject="Password Reset Request",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[target_email])
    msg.body = text
    msg.html = html

    # Send email
    try:
        mail = current_app.extensions['mail']
        mail.send(msg)
        return {"message": "Password reset email sent"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
