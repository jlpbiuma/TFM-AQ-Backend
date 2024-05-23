from flask import Blueprint
from api.controller.dashboard import *

dashboard_bp = Blueprint('dashboard', __name__)

# Get sensors by id_dashboard endpoint
dashboard_bp.add_url_rule('/estacion/<string:id_estacion>', view_func=get_dashboard_by_id_estacion, methods=['GET'])
