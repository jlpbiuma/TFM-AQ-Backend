from flask_mail import Mail
import os

mail = None

def setup_mail(app):
    global mail
    app.config['MAIL_SERVER'] = os.environ.get('EMAIL_SERVER','')
    app.config['MAIL_PORT'] = int(os.environ.get('EMAIL_PORT', 465 ))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_BOT','')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD_TFM','')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_BOT','')
    app.config['MAIL_MAX_EMAILS'] = None
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
    Mail(app)
    return mail