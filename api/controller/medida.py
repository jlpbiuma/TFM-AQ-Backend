from flask import jsonify, request
from api.model import Medida, Unidad
from api.database import mysql_db
from datetime import datetime
from sqlalchemy import desc

def create_medida():
    data = request.get_json()
    new_medida = Medida(
        ID_UNIDAD=data.get('id_unidad'),
        VALOR=data.get('valor'),
        FECHA_HORA=data.get('fecha_hora')
    )
    mysql_db.session.add(new_medida)
    mysql_db.session.commit()
    return jsonify(new_medida.to_dict()), 201

def get_medida_by_id(id_medida):
    medida = Medida.query.get(id_medida)
    if medida is None:
        return jsonify({'error': 'Medida not found'}), 404
    return jsonify(medida.to_dict()), 200

def get_medidas():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    medidas = Medida.query.paginate(page=page, per_page=per_page, error_out=False)
    medidas_dict = [medida.to_dict() for medida in medidas.items]
    return jsonify({
        'medidas': medidas_dict,
        'total': medidas.total,
        'pages': medidas.pages,
        'current_page': medidas.page
    }), 200

def get_last_medidas():
    medidas = Medida.query.order_by(Medida.FECHA_HORA.desc()).limit(10).all()
    medidas_dict = [medida.to_dict() for medida in medidas]
    return jsonify(medidas_dict), 200

def get_last_medidas_by_unidad(id_unidad):
    medidas = Medida.query.filter_by(ID_UNIDAD=id_unidad).order_by(Medida.FECHA_HORA.desc()).limit(10).all()
    medidas_dict = [medida.to_dict() for medida in medidas]
    return jsonify(medidas_dict), 200

def get_medidas_by_id_estacion(id_estacion):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    medidas = Medida.query.join(Unidad).filter(Unidad.ID_ESTACION == id_estacion).paginate(page=page, per_page=per_page, error_out=False)
    medidas_dict = [medida.to_dict() for medida in medidas.items]
    return jsonify({
        'medidas': medidas_dict,
        'total': medidas.total,
        'pages': medidas.pages,
        'current_page': medidas.page
    }), 200

def get_medidas_by_id_estacion_id_unidad(id_estacion, id_unidad):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    medidas = Medida.query.join(Unidad).filter(Unidad.ID_ESTACION == id_estacion, Unidad.ID_UNIDAD == id_unidad).paginate(page=page, per_page=per_page, error_out=False)
    medidas_dict = [medida.to_dict() for medida in medidas.items]
    return jsonify({
        'medidas': medidas_dict,
        'total': medidas.total,
        'pages': medidas.pages,
        'current_page': medidas.page
    }), 200

def get_medidas_by_id_estacion_id_unidad_last(id_estacion, id_unidad):
    medida = Medida.query\
        .join(Unidad)\
        .filter(Unidad.ID_ESTACION == id_estacion, Unidad.ID_UNIDAD == id_unidad)\
        .order_by(desc(Medida.FECHA_HORA))\
        .first()

    if medida is None:
        return jsonify({'error': 'No medidas found for the specified estacion and unidad'}), 404

    return jsonify(medida.to_dict()), 200

def get_medida_by_id_estacion_last(id_estacion):
    medida = Medida.query\
        .join(Unidad)\
        .filter(Unidad.ID_ESTACION == id_estacion)\
        .order_by(desc(Medida.FECHA_HORA))\
        .first()

    if medida is None:
        return jsonify({'error': 'No medida found for the specified estacion'}), 404

    return jsonify(medida.to_dict()), 200

def update_medida_by_id(id_medida):
    medida = Medida.query.get(id_medida)
    if medida is None:
        return jsonify({'error': 'Medida not found'}), 404
    data = request.get_json()
    medida.ID_UNIDAD = data.get('id_unidad', medida.ID_UNIDAD)
    medida.VALOR = data.get('valor', medida.VALOR)
    if 'fecha_hora' in data:
        medida.FECHA_HORA = datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M:%S')
    mysql_db.session.commit()
    return jsonify(medida.to_dict()), 200

def delete_medida_by_id(id_medida):
    medida = Medida.query.get(id_medida)
    if medida is None:
        return jsonify({'error': 'Medida not found'}), 404
    mysql_db.session.delete(medida)
    mysql_db.session.commit()
    return jsonify(medida.to_dict()), 200
