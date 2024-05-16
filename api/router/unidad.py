from flask import Blueprint
from api.controller.unidad import *

unidad_bp = Blueprint('unidad', __name__)

unidad_bp.add_url_rule('/create', view_func=create_unidad, methods=['POST'])
