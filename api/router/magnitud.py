from flask import Blueprint
from api.controller.magnitud import *

magnitud_bp = Blueprint('magnitud', __name__)

# Define the routes
magnitud_bp.add_url_rule('/create', view_func=create_magnitud, methods=['POST'])
magnitud_bp.add_url_rule('/', view_func=get_magnitudes, methods=['GET'])
magnitud_bp.add_url_rule('/posibles', view_func=get_posibles_magnitudes, methods=['GET'])
magnitud_bp.add_url_rule('/<int:id_magnitud>', view_func=get_magnitud_by_id, methods=['GET'])
magnitud_bp.add_url_rule('/<int:id_magnitud>', view_func=update_magnitud_by_id, methods=['PUT'])
magnitud_bp.add_url_rule('/<int:id_magnitud>', view_func=delete_magnitud_by_id, methods=['DELETE'])
