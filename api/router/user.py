from flask import Blueprint
from api.controller.user import *
from api.database import *

user_bp = Blueprint('user', __name__)

user_bp.record_once(mysql_conector)
user_bp.add_url_rule('/create', view_func=create_user, methods=['POST'])
