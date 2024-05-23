import os

class Mailing(object):
    MAIL_SERVER = os.environ.get('EMAIL_SERVER','')
    MAIL_PORT = os.environ.get('EMAIL_PORT','')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_BOT','')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD_TFM','')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_BOT','')
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False