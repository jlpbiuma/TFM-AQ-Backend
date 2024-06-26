from flask import jsonify, request
from api.model import Estacion, EstacionesMagnitudes, Magnitud
from api.database import mysql_db
from api.controller.estaciones_usuarios import delete_all_links_estacion_usuario
from api.controller.estaciones_dispositivos import delete_all_links_estacion_dispositivo
from api.controller.medida import delete_all_medidas_by_id_estacion
from api.controller.tools.ip import encrypt_ip, decrypt_estacion_ip

def create_estacion():
    data = request.get_json()
    new_estacion = Estacion(
        NOMBRE=data.get('nombre'),
        LOCALIZACION=data.get('localizacion'),
        ID_ADMINISTRADOR=1
    )
    mysql_db.session.add(new_estacion)
    mysql_db.session.commit()
    return jsonify(new_estacion.to_dict()), 201

def get_estaciones():
    estaciones = Estacion.query.all()
    estaciones_dict = [decrypt_estacion_ip(estacion.to_dict()) for estacion in estaciones]
    return jsonify(estaciones_dict), 200

def get_estacion_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    # Get the all the associated links from the EstacionesMagnitudes table
    estaciones_magnitudes = EstacionesMagnitudes.query.filter_by(ID_ESTACION=id_estacion).all()
    # Add topics to estacione dict
    topics = []
    for estacion_magnitud in estaciones_magnitudes:
        topic = f'estacion/{id_estacion}/magnitud/{estacion_magnitud.ID_MAGNITUD}'
        magnitud = Magnitud.query.get(estacion_magnitud.ID_MAGNITUD)
        topics.append({
            'topic_str': topic,
            'magnitud': magnitud.to_dict()
        })
    estacion_dict = estacion.to_dict()
    estacion_dict['topics'] = topics
    return jsonify(decrypt_estacion_ip(estacion_dict)), 200
    # return jsonify(decrypt_estacion_ip(estacion.to_dict())), 200

def update_gateway_ip_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404

    data = request.get_json()
    public_ip = data.get('public_ip')
    timestamp = data.get('timestamp')
    # Get the ip from the request
    ip_local = request.remote_addr
    
    if public_ip:
        # Encrypt the IP address before storing it
        encrypted_ip = encrypt_ip(public_ip)
        estacion.IP_GATEWAY = encrypted_ip
    
    if ip_local:
        estacion.IP_LOCAL = ip_local
    
    if timestamp:
        estacion.FECHA_HORA_IP = timestamp

    # Update the estacion
    mysql_db.session.commit()
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
    delete_all_links_estacion_usuario(id_estacion)  # Delete associated links first
    delete_all_links_estacion_dispositivo(id_estacion)  # Delete associated links first
    delete_all_medidas_by_id_estacion(id_estacion)  # Delete associated medidas first
    mysql_db.session.delete(estacion)
    mysql_db.session.commit()
    return jsonify(estacion.to_dict()), 200

