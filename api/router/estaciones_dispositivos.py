from flask import Blueprint
from api.controller.estaciones_dispositivos import *

estaciones_dispositivos_bp = Blueprint('estaciones_dispositivos', __name__)

# Create
estaciones_dispositivos_bp.add_url_rule('/<int:id_estacion>', view_func=link_estacion_by_id_to_id_dispositivo, methods=['POST'])

# Read
estaciones_dispositivos_bp.add_url_rule('/<int:id_estacion>', view_func=get_dispositivos_by_estacion, methods=['GET'])

# Update
estaciones_dispositivos_bp.add_url_rule('/<int:id_estacion>', view_func=update_link_estacion_dispositivo, methods=['PUT'])

# Delete
estaciones_dispositivos_bp.add_url_rule('/<int:id_estacion>', view_func=delete_link_estacion_dispositivo, methods=['DELETE'])
