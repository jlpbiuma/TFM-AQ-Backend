from flask import Blueprint
from api.controller.usuario import *

usuario_bp = Blueprint('usuario', __name__)

# Create usuario endpoint
usuario_bp.add_url_rule('/create', view_func=create_usuario, methods=['POST'])

# Get usuario by ID endpoint
usuario_bp.add_url_rule('/<string:usuario_id>', view_func=get_usuario, methods=['GET'])

# Get usuario list endpoint with pagination support
usuario_bp.add_url_rule('/', view_func=get_usuario_list, methods=['GET'])

# Update usuario by ID endpoint
usuario_bp.add_url_rule('/<string:usuario_id>', view_func=update_usuario, methods=['PUT'])

# Delete usuario by ID endpoint
usuario_bp.add_url_rule('/<string:usuario_id>', view_func=delete_usuario, methods=['DELETE'])
