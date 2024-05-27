from flask import Blueprint
from api.controller.estaciones_usuarios import *

estaciones_usuarios_bp = Blueprint('estaciones_usuarios', __name__)

# Create
estaciones_usuarios_bp.add_url_rule('/<int:id_estacion>', view_func=link_estacion_by_id_to_id_usuario, methods=['POST'])

# Read
estaciones_usuarios_bp.add_url_rule('/mis-estaciones/<string:id_usuario>', view_func=get_estaciones_by_usuario, methods=['GET'])
estaciones_usuarios_bp.add_url_rule('/<int:id_estacion>', view_func=get_usuarios_by_estacion, methods=['GET'])
estaciones_usuarios_bp.add_url_rule('/no-estacion/<int:id_estacion>', view_func=get_all_users_without_id_estacion, methods=['GET'])


# Update
estaciones_usuarios_bp.add_url_rule('/<int:id_estacion>', view_func=update_link_estacion_usuario, methods=['PUT'])

# Delete
estaciones_usuarios_bp.add_url_rule('/<int:id_estacion>', view_func=delete_link_estacion_usuario, methods=['DELETE'])
estaciones_usuarios_bp.add_url_rule('/<int:id_estacion>/usuario/<string:id_usuario>', view_func=delete_estacion_usuario_by_id_usuario_id_estacion, methods=['DELETE'])
