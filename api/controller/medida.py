from flask import jsonify, request
from api.model import Medida, Magnitud
from api.database import mysql_db
from datetime import datetime
from sqlalchemy import desc, and_


def create_medida():
    # TODO: 1. Traducir el código de todas las unidades que tiene el dispositivo
    data = request.get_json()
    new_medida = Medida(
        ID_MAGNITUD=data.get('id_unidad'),
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

def get_last_medidas_by_id_magnitud(id_magnitud):
    medidas = Medida.query.filter_by(ID_MAGNITUD=id_magnitud).order_by(Medida.FECHA_HORA.desc()).limit(10).all()
    medidas_dict = [medida.to_dict() for medida in medidas]
    return jsonify(medidas_dict), 200

def get_medidas_by_id_estacion(id_estacion):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Paginate the Medida query
    medidas_pagination = Medida.query.filter_by(ID_ESTACION=id_estacion).order_by(Medida.FECHA_HORA).paginate(page=page, per_page=per_page, error_out=False)
    
    medidas = medidas_pagination.items
    
    # Extract all unique ID_MAGNITUD values
    id_magnitudes = list(set(medida.ID_MAGNITUD for medida in medidas))
    
    # Fetch all Magnitudes at once
    magnitudes = Magnitud.query.filter(Magnitud.ID_MAGNITUD.in_(id_magnitudes)).all()
    
    # Map Magnitudes by their ID
    magnitudes_dict = {magnitud.ID_MAGNITUD: magnitud.to_dict() for magnitud in magnitudes}
    
    # Group Medidas by Magnitude
    grouped_medidas = {}
    for medida in medidas:
        magnitud = magnitudes_dict[medida.ID_MAGNITUD]
        magnitud_name = magnitud['magnitud']
        if magnitud_name in grouped_medidas:
            grouped_medidas[magnitud_name].append(medida.to_dict())
        else:
            grouped_medidas[magnitud_name] = [medida.to_dict()]
    
    return jsonify({
        'medidas': grouped_medidas,
        'total': medidas_pagination.total,
        'pages': medidas_pagination.pages,
        'current_page': medidas_pagination.page
    }), 200

def get_medidas_by_id_estacion_id_magnitud(id_estacion, id_magnitud):
    # Get the start and end dates from query parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    if not start_date_str or not end_date_str:
        return jsonify({'error': 'Start date and end date are required'}), 400
    
    try:
        # Parse the date strings into datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400
    
    if start_date > end_date:
        return jsonify({'error': 'Start date must be before end date'}), 400
    
    # Filter by ID_ESTACION, ID_MAGNITUD, and the date range
    medidas_query = Medida.query.filter(
        and_(
            Medida.ID_ESTACION == id_estacion,
            Medida.ID_MAGNITUD == id_magnitud,
            Medida.FECHA_HORA.between(start_date, end_date)
        )
    ).order_by(Medida.FECHA_HORA)
    
    medidas = medidas_query.all()
    
    # Get the total count of medidas for the given estacion, magnitud, and date range
    total_count = medidas_query.count()
    
    medidas_dict = [medida.to_dict() for medida in medidas]
    
    return jsonify({
        'medidas': medidas_dict,
        'total': total_count
    }), 200

def get_medidas_by_id_estacion_id_magnitud_last(id_estacion, id_unidad):
    medida = Medida.query\
        .join(Unidad)\
        .filter(Unidad.ID_ESTACION == id_estacion, Unidad.ID_MAGNITUD == id_unidad)\
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
    medida.ID_MAGNITUD = data.get('id_unidad', medida.ID_MAGNITUD)
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

def delete_all_medidas_by_id_estacion(id_estacion):
    medidas = Medida.query.filter_by(ID_ESTACION=id_estacion).all()
    for medida in medidas:
        mysql_db.session.delete(medida)
    mysql_db.session.commit()
    return jsonify({'message': 'All medidas deleted successfully'}), 200