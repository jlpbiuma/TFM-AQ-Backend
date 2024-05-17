from flask import Blueprint, jsonify, request
from api.controller.auth import login

auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
