from flask import Blueprint
from api.controller.test import *

test_bp = Blueprint('test', __name__)

test_bp.add_url_rule('/get-test', view_func=get_test, methods=['POST'])
test_bp.add_url_rule('/create-test', view_func=create_test, methods=['POST'])
