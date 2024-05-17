from flask import Blueprint
from api.controller.auth import *

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/register', view_func=register, methods=['POST'])
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/forgot-password', view_func=forgot_password, methods=['POST'])
auth_bp.add_url_rule('/reset-password', view_func=reset_password, methods=['POST'])
