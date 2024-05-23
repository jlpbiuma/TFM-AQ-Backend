from flask import Flask, Blueprint
from flask_cors import CORS
from api.router import *
from api.database import *
from api.middleware import *

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_cors()
        self.init_database_connections()
        self.register_blueprints()
        # self.register_middlewares()

    def configure_cors(self):
        CORS(self.app, origins="*", allow_headers="*")

    def register_blueprints(self):
        bp = Blueprint('api', __name__)
        self.app.register_blueprint(dispositivo_bp, url_prefix='/api/dispositivo')
        self.app.register_blueprint(estacion_bp, url_prefix='/api/estacion')
        self.app.register_blueprint(medida_bp, url_prefix='/api/medida')
        self.app.register_blueprint(sensor_bp, url_prefix='/api/sensor')
        self.app.register_blueprint(usuario_bp, url_prefix='/api/usuario')
        self.app.register_blueprint(unidad_bp, url_prefix='/api/unidad')
        self.app.register_blueprint(magnitud_bp, url_prefix='/api/magnitud')
        self.app.register_blueprint(auth_bp, url_prefix='/api/auth')
        self.app.register_blueprint(estaciones_dispositivos_bp, url_prefix='/api/estacion/dispositivo')
        self.app.register_blueprint(estaciones_usuarios_bp, url_prefix='/api/estacion/usuario')
        self.app.register_blueprint(bp)
    
    def register_middlewares(self):
        self.app.after_request(config_headers)

    def init_database_connections(self):
        self.mysql = setup_mysql_connection(self.app)
        self.mongo_db = mongo_db

    def run(self, **kwargs):
        self.app.run(**kwargs)