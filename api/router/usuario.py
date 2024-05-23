from flask import Blueprint
from api.controller.usuario import *
from api.middleware import *

usuario_bp = Blueprint('usuario', __name__)

# Create usuario endpoint
usuario_bp.add_url_rule('/create', view_func=create_usuario, methods=['POST'])

# Get usuario by ID endpoint
usuario_bp.add_url_rule('/<string:id_usuario>', view_func=is_this_client_usuario(get_usuario), methods=['GET'])

# Get usuario list endpoint with pagination support
usuario_bp.add_url_rule('/', view_func=get_usuario_list, methods=['GET'])

# Update usuario by ID endpoint
usuario_bp.add_url_rule('/<string:id_usuario>', view_func=is_this_client_usuario(update_usuario), methods=['PUT'])

# Delete usuario by ID endpoint
usuario_bp.add_url_rule('/<string:id_usuario>', view_func=delete_usuario, methods=['DELETE'])
