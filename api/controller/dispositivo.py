# dispositivo_controller.py
from flask import jsonify, request
from api.model.dispositivo import Dispositivo
from api.model.estaciones_link import EstacionesMagnitudes
from api.database import mysql_db

def create_dispositivo():
    data = request.get_json()
    nombre = data.get('nombre')
    localizacion = data.get('localizacion')
    estado = 'Online'
    id_estacion = data.get('id_estacion')
    ids_magnitudes = data.get('magnitudes')

    if not nombre or not localizacion or not estado:
        return jsonify({'error': 'Nombre, localizacion, and estado are required'}), 400
    
    dispositivo = Dispositivo(nombre, localizacion, estado, id_estacion)
    dispositivo = dispositivo.save()
    
    # Create a new link between the estacion and the magnitudes
    for id_magnitud in ids_magnitudes:
        new_estacion_magnitud = EstacionesMagnitudes(
            ID_ESTACION=id_estacion,
            ID_MAGNITUD=id_magnitud
        )
        mysql_db.session.add(new_estacion_magnitud)
    mysql_db.session.commit()
    
    return jsonify(dispositivo), 201

def get_dispositivo(dispositivo_id):
    dispositivo = Dispositivo.get_dispositivo_by_id(dispositivo_id)
    if dispositivo:
        return jsonify(dispositivo), 200
    else:
        return jsonify({'error': 'Dispositivo not found'}), 404

def get_dispositivo_list():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    dispositivos = Dispositivo.get_dispositivos_by_pagination(page, per_page)
    return jsonify(dispositivos), 200

def get_dispositivo_by_id_estacion(id_estacion):
    dispositivo = Dispositivo.get_dispositivo_by_id_estacion(id_estacion)
    return jsonify(dispositivo), 200

def update_dispositivo(dispositivo_id):
    data = request.get_json()
    dispositivo = Dispositivo.get_dispositivo_by_id(dispositivo_id)
    if dispositivo:
        dispositivo = Dispositivo.update_dispositivo_by_id(dispositivo_id, data)
        return jsonify(dispositivo), 200
    else:
        return jsonify({'error': 'Dispositivo not found'}), 404

# You might also want to define a delete method for dispositivos, even though it wasn't explicitly requested:
def delete_dispositivo(dispositivo_id):
    dispositivo = Dispositivo.get_dispositivo_by_id(dispositivo_id)
    if dispositivo:
        dispositivo = Dispositivo.delete_dispositivo_by_id(dispositivo_id)
        return jsonify(dispositivo), 200
    else:
        return jsonify({'error': 'Dispositivo not found'}), 404
