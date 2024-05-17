from flask import Blueprint
from api.controller.estacion import *

estacion_bp = Blueprint('estacion', __name__)

# Define the routes
estacion_bp.add_url_rule('/create', view_func=create_estacion, methods=['POST'])
estacion_bp.add_url_rule('/', view_func=get_estaciones, methods=['GET'])
estacion_bp.add_url_rule('/<int:id_estacion>', view_func=get_estacion_by_id, methods=['GET'])
estacion_bp.add_url_rule('/<int:id_estacion>', view_func=update_estacion_by_id, methods=['PUT'])
estacion_bp.add_url_rule('/<int:id_estacion>', view_func=delete_estacion_by_id, methods=['DELETE'])

