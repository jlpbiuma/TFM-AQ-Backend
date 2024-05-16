from flask import Blueprint
from api.controller.dispositivo import *

dispositivo_bp = Blueprint('dispositivo', __name__)

dispositivo_bp.add_url_rule('/create', view_func=create_dispositivo, methods=['POST'])
