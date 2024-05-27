from flask import jsonify, request
from api.model import Estacion, Usuario, EstacionesUsuarios
from api.database import mysql_db
from api.database.mysql_connection import mysql_db
from sqlalchemy.sql import not_

# Create link between Estacion and Usuario
def link_estacion_by_id_to_id_usuario(id_estacion):
    estacion = Estacion.query.get(id_estacion)
    if estacion is None:
        return jsonify({'error': 'Estacion not found'}), 404

    # Get the list of user IDs from the request body
    ids_usuarios = request.get_json('ids_usuarios').get('ids_usuarios')
    if not ids_usuarios:
        return jsonify({'error': 'No user IDs provided'}), 400

    # Fetch the users with the provided IDs
    users = Usuario.get_multiple_users_by_ids(ids_usuarios)
    if not users:
        return jsonify({'error': 'Some or all users not found'}), 404

    # Create a new EstacionesUsuarios entry for each user ID
    new_links = []
    for id_usuario in ids_usuarios:
        # First verify that the link does not already exist
        link = EstacionesUsuarios.query.filter_by(ID_ESTACION=id_estacion, ID_USUARIO=id_usuario).first()
        if link:
            continue
        new_link_estacion_usuario = EstacionesUsuarios(
            ID_ESTACION=id_estacion,
            ID_USUARIO=id_usuario
        )
        mysql_db.session.add(new_link_estacion_usuario)
        new_links.append(new_link_estacion_usuario)

    # Commit all the new links to the database
    mysql_db.session.commit()

    # Return the new links as a list of dictionaries
    return jsonify(ids_usuarios), 201

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

def get_all_users_without_id_estacion(id_estacion):
    links = EstacionesUsuarios.query.filter(not_(EstacionesUsuarios.ID_ESTACION == id_estacion)).all()
    usuarios = []
    for link in links:
        user = Usuario.get_user_by_id(link.ID_USUARIO)
        if user:
            usuarios.append(user)
    return jsonify(usuarios), 200

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

# Delete link between Estacion and Usuario
def delete_all_links_estacion_usuario(id_estacion):
    links = EstacionesUsuarios.query.filter_by(ID_ESTACION=id_estacion).all()
    if not links:
        return jsonify({'error': 'Links not found for this Estacion'}), 404
    for link in links:
        mysql_db.session.delete(link)
    mysql_db.session.commit()
    return jsonify({'message': 'Links deleted successfully'}), 200

def delete_estacion_usuario_by_id_usuario_id_estacion(id_usuario, id_estacion):
    link = EstacionesUsuarios.query.filter_by(ID_ESTACION=id_estacion, ID_USUARIO=id_usuario).first()
    if link is None:
        return jsonify({'error': 'Link not found'}), 404
    mysql_db.session.delete(link)
    mysql_db.session.commit()
    # Get the user by id
    user = Usuario.get_user_by_id(id_usuario)
    return jsonify(user), 200