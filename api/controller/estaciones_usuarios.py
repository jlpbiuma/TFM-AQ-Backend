from flask import jsonify, request
from api.model import Estacion, Usuario, EstacionesUsuarios
from api.database import mysql_db

# Create link between Estacion and Usuario
def link_estacion_by_id_to_id_usuario(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    user = Usuario.get_user_by_id(id_usuario)
    if user is None:
        return jsonify({'error': 'Usuario not found'}), 404
    new_link_estacion_usuario = EstacionesUsuarios(
        ID_ESTACION=id_estacion,
        ID_USUARIO=id_usuario
    )
    mysql_db.session.add(new_link_estacion_usuario)
    mysql_db.session.commit()
    return jsonify(new_link_estacion_usuario.to_dict()), 201

# Read links between Estacion and Usuario
def get_usuarios_by_estacion(id_estacion):
    links = EstacionesUsuarios.query.filter_by(ID_ESTACION=id_estacion).all()
    usuarios = []
    for link in links:
        user = Usuario.get_user_by_id(link.ID_USUARIO)
        if user:
            usuarios.append(user)
    return jsonify(usuarios), 200

def get_estaciones_by_usuario(id_usuario):
    links = EstacionesUsuarios.query.filter_by(ID_USUARIO=id_usuario).all()
    estaciones = []
    for link in links:
        estacion = Estacion.query.get(link.ID_ESTACION).to_dict()
        if estacion:
            estaciones.append(estacion)
    return jsonify(estaciones), 200

# Update link between Estacion and Usuario
def update_link_estacion_usuario(id_estacion):
    link = EstacionesUsuarios.query.filter_by(ID_ESTACION=id_estacion).first()
    if link is None:
        return jsonify({'error': 'Link not found'}), 404
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    user = Usuario.get_user_by_id(id_usuario)
    if user is None:
        return jsonify({'error': 'Usuario not found'}), 404
    link.ID_USUARIO = id_usuario
    mysql_db.session.commit()
    return jsonify(link.to_dict()), 200

# Delete link between Estacion and Usuario
def delete_link_estacion_usuario(id_estacion):
    link = EstacionesUsuarios.query.filter_by(ID_ESTACION=id_estacion).first()
    if link is None:
        return jsonify({'error': 'Link not found'}), 404
    mysql_db.session.delete(link)
    mysql_db.session.commit()
    return jsonify({'message': 'Link deleted successfully'}), 200