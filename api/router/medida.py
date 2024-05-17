from flask import Blueprint
from api.controller.medida import *

medida_bp = Blueprint('medida', __name__)

medida_bp.add_url_rule('/create', view_func=create_medida, methods=['POST'])
medida_bp.add_url_rule('/<int:id_medida>', view_func=get_medida_by_id, methods=['GET'])
medida_bp.add_url_rule('/', view_func=get_medidas, methods=['GET'])
medida_bp.add_url_rule('/last', view_func=get_last_medidas, methods=['GET'])
medida_bp.add_url_rule('/last/<int:id_unidad>', view_func=get_last_medidas_by_unidad, methods=['GET'])
medida_bp.add_url_rule('/estacion/<int:id_estacion>', view_func=get_medidas_by_id_estacion, methods=['GET'])
medida_bp.add_url_rule('/estacion/<int:id_estacion>/unidad/<int:id_unidad>', view_func=get_medidas_by_id_estacion_id_unidad, methods=['GET'])
medida_bp.add_url_rule('/estacion/<int:id_estacion>/unidad/<int:id_unidad>/last', view_func=get_medidas_by_id_estacion_id_unidad_last, methods=['GET'])
medida_bp.add_url_rule('/estacion/<int:id_estacion>/last', view_func=get_medida_by_id_estacion_last, methods=['GET'])
medida_bp.add_url_rule('/<int:id_medida>', view_func=update_medida_by_id, methods=['PUT'])
medida_bp.add_url_rule('/<int:id_medida>', view_func=delete_medida_by_id, methods=['DELETE'])
