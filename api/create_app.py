from flask import Flask, Blueprint
from api.router import *
from api.database import *
from api.middleware import *

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.init_database_connections()
        self.register_blueprints()
        self.register_middlewares()

    def register_blueprints(self):
        bp = Blueprint('api', __name__)
        self.app.register_blueprint(dispositivo_bp, url_prefix='/api/dispositivo')
        self.app.register_blueprint(estacion_bp, url_prefix='/api/estacion')
        self.app.register_blueprint(medida_bp, url_prefix='/api/medida')
        self.app.register_blueprint(sensor_bp, url_prefix='/api/sensor')
        self.app.register_blueprint(user_bp, url_prefix='/api/user')
        self.app.register_blueprint(unidad_bp, url_prefix='/api/unidad')
        self.app.register_blueprint(bp)
    
    def register_middlewares(self):
        self.app.after_request(config_headers)

    def init_database_connections(self):
        self.mysql = setup_mysql_connection(self.app)
        self.mongo_db = setup_mongo_connection()

    def run(self, **kwargs):
        self.app.run(**kwargs)