from flask import Blueprint
from api.controller.sensor import *

sensor_bp = Blueprint('sensor', __name__)

sensor_bp.add_url_rule('/create', view_func=create_sensor, methods=['POST'])
