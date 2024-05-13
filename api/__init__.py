from flask import Flask, Blueprint
from api.router import *

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.register_blueprints()

    def register_blueprints(self):
        bp = Blueprint('api', __name__)
        print("Working here!")
        self.app.register_blueprint(test_bp, url_prefix='/api/test')
        self.app.register_blueprint(medida_bp, url_prefix='/api/medida')
        self.app.register_blueprint(sensor_bp, url_prefix='/api/sensor')
        self.app.register_blueprint(bp)
    
    def register_middleware(self):
        @self.app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            return response
        
    def run(self, **kwargs):
        self.app.run(**kwargs)
