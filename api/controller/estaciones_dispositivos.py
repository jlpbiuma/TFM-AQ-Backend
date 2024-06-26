from flask import jsonify, request
from api.model import Estacion, Dispositivo, EstacionesDispositivos
from api.database import mysql_db
from sqlalchemy.sql import not_

# Create link between Estacion and Dispositivo
def link_estacion_by_id_to_id_dispositivo(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404

    data = request.get_json()
    id_dispositivos = data.get('id_dispositivo')
    dispositivos = []
    for id in id_dispositivos:
        dispositivo = Dispositivo.get_dispositivo_by_id(id)
        if dispositivo:
            dispositivos.append(dispositivo)
    
    if not dispositivos:
        return jsonify({'error': 'No valid Dispositivo found'}), 404

    for dispositivo in dispositivos:
        id_dispositivo = dispositivo['id_dispositivo']
        # Verify first if the link already exists
        link = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion, ID_DISPOSITIVO=id_dispositivo).first()
        if link is not None:
            continue
        new_link_estacion_dispositivo = EstacionesDispositivos(
            ID_ESTACION=id_estacion,
            ID_DISPOSITIVO=id_dispositivo
        )
        mysql_db.session.add(new_link_estacion_dispositivo)

    mysql_db.session.commit()
    # Return an array of the new dispositivos
    return jsonify(dispositivos), 201

# Read links between Estacion and Dispositivo
def get_dispositivos_by_estacion(id_estacion):
    links = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).all()
    dispositivos = []
    for link in links:
        dispositivo = Dispositivo.get_dispositivo_by_id(link.ID_DISPOSITIVO)
        if dispositivo:
            dispositivos.append(dispositivo)
    return jsonify(dispositivos), 200

def get_all_dispositivos_without_id_estacion(id_estacion):
    # Get the list of user IDs with this id_estacion in the EstacionesDispositivos collection
    ids_dispositivos = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).all()
    # Get the ids_dispositivos
    ids_dispositivos = [link.ID_DISPOSITIVO for link in ids_dispositivos]

    # Get all users that are not in the list of ids_dispositivos in the Usuarios collection
    if ids_dispositivos:
        dispositivos = Dispositivo.get_negate_ids_dispositivos(ids_dispositivos)
    else:
        dispositivos = Dispositivo.get_all_dispositivos()

    # Convert the cursor to a list and then to JSON
    dispositivos_list = list(dispositivos)
    # Cast the list to JSON and return
    return jsonify(dispositivos_list), 200

# Update link between Estacion and Dispositivo
def update_link_estacion_dispositivo(id_estacion):
    link = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).first()
    if link is None:
        return jsonify({'error': 'Link not found'}), 404
    data = request.get_json()
    id_dispositivo = data.get('id_dispositivo')
    dispositivo = Dispositivo.get_dispositivo_by_id(id_dispositivo)
    if dispositivo is None:
        return jsonify({'error': 'Dispositivo not found'}), 404
    link.ID_DISPOSITIVO = id_dispositivo
    mysql_db.session.commit()
    return jsonify(link.to_dict()), 200

# Delete link between Estacion and Dispositivo
def delete_link_estacion_dispositivo(id_estacion):
    link = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).first()
    if link is None:
        return jsonify({'error': 'Link not found'}), 404
    mysql_db.session.delete(link)
    mysql_db.session.commit()
    return jsonify({'message': 'Link deleted successfully'}), 200

def delete_all_links_estacion_dispositivo(id_estacion):
    links = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).all()
    if not links:
        return jsonify({'error': 'Links not found for this Estacion'}), 404
    for link in links:
        mysql_db.session.delete(link)
    mysql_db.session.commit()
    return jsonify({'message': 'All links deleted successfully'}), 200

def delete_estacion_dispositivo_by_id_dispositivo_id_estacion(id_estacion, id_dispositivo):
    links = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).all()
    for link in links:
        mysql_db.session.delete(link)
    mysql_db.session.commit()
    return jsonify({'message': 'All links deleted successfully'}), 200
