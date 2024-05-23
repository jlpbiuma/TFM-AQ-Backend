import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.controller.tools import generate_token
import os

def send_password_reset_email(target_email):
    # Generate token

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
            return {"message": "Password reset email sent"}, 200
        except smtplib.SMTPAuthenticationError:
            # Failed to login due to incorrect credentials
            return {"error": "Failed to login with provided email credentials"}, 401
        except Exception as e:
            # Other exceptions (e.g., network issues)
            return {"error": str(e)}, 500