from flask import Blueprint
from api.controller.unidad import *

unidad_bp = Blueprint('unidad', __name__)

unidad_bp.add_url_rule('/create', view_func=create_unidad, methods=['POST'])
unidad_bp.add_url_rule('/', view_func=get_unidades, methods=['GET'])
unidad_bp.add_url_rule('<int:id_unidad>', view_func=get_unidad_by_id, methods=['GET'])
unidad_bp.add_url_rule('/estacion/<int:id_estacion>', view_func=get_unidad_by_id_estacion, methods=['GET'])
unidad_bp.add_url_rule('<int:id_unidad>', view_func=update_unidad_by_id, methods=['PUT'])
unidad_bp.add_url_rule('<int:id_unidad>', view_func=delete_unidad_by_id, methods=['DELETE'])
