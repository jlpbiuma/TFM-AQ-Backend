from flask import jsonify, request
from api.model import Estacion
from api.database import mysql_db

def create_estacion():
    data = request.get_json()
    new_estacion = Estacion(
        ID_ADMINISTRADOR=data.get('id_administrador'),
        NOMBRE=data.get('nombre'),
        LOCALIZACION=data.get('localizacion')
    )
    mysql_db.session.add(new_estacion)
    mysql_db.session.commit()
    return jsonify(new_estacion.to_dict()), 201

def get_estaciones():
    estaciones = Estacion.query.all()
    estaciones_dict = [estacion.to_dict() for estacion in estaciones]
    return jsonify(estaciones_dict), 200

def get_estacion_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    return jsonify(estacion.to_dict()), 200

def update_estacion_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    data = request.get_json()
    estacion.ID_ADMINISTRADOR = data.get('id_administrador', estacion.ID_ADMINISTRADOR)
    estacion.NOMBRE = data.get('nombre', estacion.NOMBRE)
    estacion.LOCALIZACION = data.get('localizacion', estacion.LOCALIZACION)
    mysql_db.session.commit()
    return jsonify(estacion.to_dict()), 200

def delete_estacion_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    mysql_db.session.delete(estacion)
    mysql_db.session.commit()
    return jsonify(estacion.to_dict()), 200

