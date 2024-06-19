from flask import jsonify, request
from api.database import mysql_db

# Define the function to create a new Unidad
def create_unidad():
    data = request.get_json()
    
    if not data or 'id_magnitud' not in data or 'id_estacion' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    id_magnitud = int(data['id_magnitud'])
    id_estacion = int(data['id_estacion'])
    
    # Verify that the combination of ID_MAGNITUD and ID_ESTACION does not already exist
    existing_unidad = Unidad.query.filter_by(ID_MAGNITUD=id_magnitud, ID_ESTACION=id_estacion).first()
    if existing_unidad:
        return jsonify({'error': 'Unidad with this ID_MAGNITUD and ID_ESTACION already exists'}), 400
    
    # Create the new Unidad
    new_unidad = Unidad(
        ID_MAGNITUD=id_magnitud,
        ID_ESTACION=id_estacion
    )
    try:
        mysql_db.session.add(new_unidad)
        mysql_db.session.commit()
    except:
        return jsonify({"error":"Este ID_MAGNITUD o ID_ESTACION no existe"})
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
    unidad = Unidad.query.filter_by(ID_ESTACION=id_estacion).first()
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
