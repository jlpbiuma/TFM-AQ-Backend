import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.controller.tools import generate_token
import os

def send_password_reset_email(target_email):
    # Generate token
    token = generate_token(target_email)

    # Send email
    sender_email = os.environ.get('EMAIL_BOT')
    password = os.environ.get('EMAIL_PASSWORD_TFM')
    smtp_server = os.environ.get('EMAIL_SERVER')
    smtp_port = int(os.environ.get('EMAIL_PORT'))

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = target_email

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

    # Attach plain text and HTML content to the email
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        try:
            server.login(user=sender_email, password=password)
            server.sendmail(from_addr=sender_email, to_addrs=target_email, msg=message.as_string())
            return {"message": "Password reset email sent"}, 200
        except smtplib.SMTPAuthenticationError:
            return {"error": "Failed to login with provided email credentials"}, 401
        except Exception as e:
            return {"error": str(e)}, 500
