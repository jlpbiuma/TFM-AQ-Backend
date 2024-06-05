from flask import jsonify, request
from api.model import Estacion, Magnitud
from api.database import mysql_db
from api.controller.estaciones_usuarios import delete_all_links_estacion_usuario
from api.controller.estaciones_dispositivos import delete_all_links_estacion_dispositivo
from api.controller.medida import delete_all_medidas_by_id_estacion
from api.controller.tools.ip import encrypt_ip, decrypt_estacion_ip
from api.model.estaciones_link import EstacionesMagnitudes

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
    estaciones_dict = [decrypt_estacion_ip(estacion.to_dict()) for estacion in estaciones]
    return jsonify(estaciones_dict), 200

def get_estacion_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    topics = EstacionesMagnitudes.query.filter_by(ID_ESTACION=id_estacion).all()
    if topics is None:
        return jsonify({'error': 'Topics not found'}), 404
    array_topics = []
    for topic in topics:
        magnitud = Magnitud.query.get(topic.ID_MAGNITUD)
        if magnitud is None:
            return jsonify({'error': 'Magnitud not found'}), 404
        partial_topic = {
            'id_magnitud': magnitud.ID_MAGNITUD,
            'magnitud': magnitud.MAGNITUD,
            'descripcion': magnitud.DESCRIPCION,
            'escala': magnitud.ESCALA,
            'id_estacion': estacion.ID_ESTACION,
            'topic': f'estacion/{estacion.ID_ESTACION}/magnitud/{magnitud.ID_MAGNITUD}'
        }
        array_topics.append(partial_topic)
    estacion_dict = estacion.to_dict()
    estacion_dict['topics'] = array_topics
    return jsonify(decrypt_estacion_ip(estacion_dict)), 200

def update_gateway_ip_by_id(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    data = request.get_json()
    timestamp = data.get('timestamp')
    if timestamp is None:
        return jsonify({'error': 'Timestamp is required'}), 400
    else:
        estacion.FECHA_HORA_IP = timestamp

    public_ip = data.get('public_ip')
    if public_ip:
        # Encrypt the IP address before storing it
        estacion.IP_GATEWAY = encrypt_ip(public_ip)

    private_ip = request.remote_addr
    if private_ip:
        # Encrypt the IP address before storing it
        estacion.IP_LOCAL = encrypt_ip(private_ip)

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

