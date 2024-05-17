# controller.py
from flask import jsonify
from api.model import Estacion

def create_estacion():
    estaciones = Estacion.query.all()
    estaciones_dict = [estacion.to_dict() for estacion in estaciones]
    return jsonify(estaciones_dict)
