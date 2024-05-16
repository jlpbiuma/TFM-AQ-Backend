import os
from flask_mysqldb import MySQL

def setup_mysql_connection(app):
    try:
        app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
        app.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT', 3306)
        app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
        app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_ROOT_PASSWORD', 'password')
        app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE', 'AQ')
        mysql = MySQL(app)
        return mysql
    except KeyError as e:
        raise RuntimeError(f"Environment variable {e} is not set. Make sure all required environment variables are set.")