from flask import Blueprint
from api.controller.medida import *

medida_bp = Blueprint('medida', __name__)

medida_bp.add_url_rule('/create', view_func=create_medida, methods=['POST'])
