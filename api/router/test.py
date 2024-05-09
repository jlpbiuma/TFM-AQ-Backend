from flask import Blueprint
from api.controller.test import *

test = Blueprint('test', __name__)

test.add_url_rule('/get-test', view_func=get_test, methods=['POST'])
