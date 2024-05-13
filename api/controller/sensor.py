from time import time
from flask import jsonify

def create_sensor():
    # Insertar en la tabla SENSOR la informacion de la petición*
    return jsonify({'time': time()}), 202
