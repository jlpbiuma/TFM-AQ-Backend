from flask import Blueprint
from api.controller.medida import *

medida_bp = Blueprint('medida', __name__)

medida_bp.add_url_rule('/create', view_func=create_medida, methods=['POST'])
# Get medida by id GET
# Get medidas get
# Get last medidas get
# Get last medidas by id_unidad get
# ... UPDATE, DELETE
