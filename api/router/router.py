from flask import Blueprint
from api.router import *

bp = Blueprint('api', __name__)


bp.register_blueprint(payrol_bp, url_prefix='/payrol')
bp.register_blueprint(invoice_bp, url_prefix='/invoice')