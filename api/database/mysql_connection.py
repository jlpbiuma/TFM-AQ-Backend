# setup.py
import os
from flask_sqlalchemy import SQLAlchemy

mysql_db = SQLAlchemy()

def setup_mysql_connection(app):
    global mysql_db
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/AQ')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        mysql_db.init_app(app)  # Initialize the db instance with the Flask app
        return mysql_db
    except KeyError as e:
        raise RuntimeError(f"Environment variable {e} is not set. Make sure all required environment variables are set.")
