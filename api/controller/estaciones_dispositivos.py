from flask import jsonify, request
from api.model import Estacion, Dispositivo, EstacionesDispositivos
from api.database import mysql_db

# Create link between Estacion and Dispositivo
def link_estacion_by_id_to_id_dispositivo(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    data = request.get_json()
    id_dispositivo = data.get('id_dispositivo')
    dispositivo = Dispositivo.get_dispositivo_by_id(id_dispositivo)
    if dispositivo is None:
        return jsonify({'error': 'Dispositivo not found'}), 404
    new_link_estacion_dispositivo = EstacionesDispositivos(
        ID_ESTACION=id_estacion,
        ID_DISPOSITIVO=id_dispositivo
    )
    mysql_db.session.add(new_link_estacion_dispositivo)
    mysql_db.session.commit()
    return jsonify(new_link_estacion_dispositivo.to_dict()), 201



# Read links between Estacion and Dispositivo
def get_dispositivos_by_estacion(id_estacion):
    links = EstacionesDispositivos.query.filter_by(ID_ESTACION=id_estacion).all()
    dispositivos = []
    for link in links:
        dispositivo = Dispositivo.get_dispositivo_by_id(link.ID_DISPOSITIVO)
        if dispositivo:
            dispositivos.append(dispositivo)
    return jsonify(dispositivos), 200

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
    for link in links:
        mysql_db.session.delete(link)
    mysql_db.session.commit()
    return jsonify({'message': 'All links deleted successfully'}), 200
