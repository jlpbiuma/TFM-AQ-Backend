from flask import jsonify, request
from api.model import Unidad
from api.database import mysql_db

def create_unidad():
    data = request.get_json()
    new_unidad = Unidad(
        ID_MAGNITUD=int(data.get('id_magnitud')),
        ID_ESTACION=int(data.get('id_estacion'))
    )
    mysql_db.session.add(new_unidad)
    mysql_db.session.commit()
    return jsonify(new_unidad.to_dict()), 201

def get_unidades():
    unidades = Unidad.query.all()
    unidades_dict = [unidad.to_dict() for unidad in unidades]
    return jsonify(unidades_dict), 200

def get_unidad_by_id(id_unidad):
    unidad = Unidad.query.get(id_unidad)
    if unidad is None:
        return jsonify({'error': 'Unidad not found'}), 404
    return jsonify(unidad.to_dict()), 200

def get_unidad_by_id_estacion(id_estacion):
    unidad = Unidad.query.get(id_estacion)
    if unidad is None:
        return jsonify({'error': 'Unidad not found'}), 404
    return jsonify(unidad.to_dict()), 200

def update_unidad_by_id(id_unidad):
    unidad = Unidad.query.get(id_unidad)
    if unidad is None:
        return jsonify({'error': 'Unidad not found'}), 404
    data = request.get_json()
    unidad.ID_MAGNITUD = data.get('id_magnitud', unidad.ID_MAGNITUD)
    mysql_db.session.commit()
    return jsonify(unidad.to_dict()), 200

def delete_unidad_by_id(id_unidad):
    unidad = Unidad.query.get(id_unidad)
    if unidad is None:
        return jsonify({'error': 'Unidad not found'}), 404
    mysql_db.session.delete(unidad)
    mysql_db.session.commit()
    return jsonify(unidad.to_dict()), 200
