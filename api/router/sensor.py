from flask import Blueprint
from api.controller.sensor import *

sensor_bp = Blueprint('sensor', __name__)

# Create sensor endpoint
sensor_bp.add_url_rule('/create', view_func=create_sensor, methods=['POST'])

# Get sensor by ID endpoint
sensor_bp.add_url_rule('/<string:sensor_id>', view_func=get_sensor, methods=['GET'])

# Get sensor list endpoint with pagination support
sensor_bp.add_url_rule('/', view_func=get_sensor_list, methods=['GET'])

# Get sensors by id_dispositivo endpoint
sensor_bp.add_url_rule('/dispositivo/<string:id_dispositivo>', view_func=get_sensors_by_dispositivo, methods=['GET'])

# Update sensor by ID endpoint
sensor_bp.add_url_rule('/<string:sensor_id>', view_func=update_sensor, methods=['PUT'])

# Delete sensor by ID endpoint
sensor_bp.add_url_rule('/<string:sensor_id>', view_func=delete_sensor, methods=['DELETE'])
