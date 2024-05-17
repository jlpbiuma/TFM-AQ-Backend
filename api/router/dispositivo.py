from flask import Blueprint
from api.controller.dispositivo import *

dispositivo_bp = Blueprint('dispositivo', __name__)

# Create dispositivo endpoint
dispositivo_bp.add_url_rule('/create', view_func=create_dispositivo, methods=['POST'])

# Get dispositivo by ID endpoint
dispositivo_bp.add_url_rule('/<string:dispositivo_id>', view_func=get_dispositivo, methods=['GET'])

# Get dispositivo list endpoint with pagination support
dispositivo_bp.add_url_rule('/', view_func=get_dispositivo_list, methods=['GET'])

# Get sensors by id_dispositivo endpoint
dispositivo_bp.add_url_rule('/estacion/<string:id_estacion>', view_func=get_dispositivo_by_id_estacion, methods=['GET'])

# Update dispositivo by ID endpoint
dispositivo_bp.add_url_rule('/<string:dispositivo_id>', view_func=update_dispositivo, methods=['PUT'])

# Delete dispositivo by ID endpoint
dispositivo_bp.add_url_rule('/<string:dispositivo_id>', view_func=delete_dispositivo, methods=['DELETE'])
