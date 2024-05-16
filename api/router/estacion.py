from flask import Blueprint
from api.controller.estacion import *

estacion_bp = Blueprint('estacion', __name__)

estacion_bp.add_url_rule('/create', view_func=create_estacion, methods=['POST'])
