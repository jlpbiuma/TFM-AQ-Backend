from flask import jsonify, request
from api.model import Magnitud
from api.database import mysql_db

def create_magnitud():
    data = request.get_json()
    new_magnitud = Magnitud(
        MAGNITUD=data.get('magnitud'),
        DESCRIPCION=data.get('descripcion'),
        ESCALA=data.get('escala')
    )
    mysql_db.session.add(new_magnitud)
    mysql_db.session.commit()
    return jsonify(new_magnitud.to_dict()), 201

def get_magnitudes():
    magnitud = Magnitud.query.all()
    magnitud_dict = [magnitud.to_dict() for magnitud in magnitud]
    return jsonify(magnitud_dict), 200

def get_magnitud_by_id(id_magnitud):
    magnitud = Magnitud.query.get(id_magnitud)
    if magnitud is None:
        return jsonify({'error': 'Magnitud not found'}), 404
    return jsonify(magnitud.to_dict()), 200

def update_magnitud_by_id(id_magnitud):
    magnitud = Magnitud.query.get(id_magnitud)
    if magnitud is None:
        return jsonify({'error': 'Magnitud not found'}), 404
    data = request.get_json()
    magnitud.MAGNITUD = data.get('magnitud', magnitud.MAGNITUD)
    magnitud.DESCRIPCION = data.get('descripcion', magnitud.DESCRIPCION)
    magnitud.ESCALA = data.get('escala', magnitud.ESCALA)
    mysql_db.session.commit()
    return jsonify(magnitud.to_dict()), 200

def delete_magnitud_by_id(id_magnitud):
    magnitud = Magnitud.query.get(id_magnitud)
    if magnitud is None:
        return jsonify({'error': 'Magnitud not found'}), 404
    mysql_db.session.delete(magnitud)
    mysql_db.session.commit()
    return jsonify(magnitud.to_dict()), 200
