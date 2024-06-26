# dispositivo_controller.py
from flask import jsonify, request
from api.model.dispositivo import Dispositivo
from api.model.estacion import Estacion
from api.model.estaciones_link import EstacionesMagnitudes

DISPOSITIVO_PROPERTIES = [
    "id_dispositivo",
    "ip_gateway",
    "ip_local",
    "topics",
    "name"
]

def create_dispositivo():
    data = request.get_json()
    nombre = data.get('name')
    localizacion = data.get('location')
    estado = 'Online'
    id_estacion = data.get('id_estacion')
    magnitudes = data.get('magnitudes')

    if not nombre or not localizacion or not estado:
        return jsonify({'error': 'Nombre, localizacion, and estado are required'}), 400

    topics = []
    for magnitud in magnitudes:
        topics.append(f'estacion/{id_estacion}/magnitud/{magnitud}')
        # Verify if the the id_estacion and magnitud already exists
        estacion_magnitud = EstacionesMagnitudes.query.filter_by(ID_ESTACION=id_estacion, ID_MAGNITUD=magnitud).first()
        if estacion_magnitud:
            continue
        # Insert into EstacionesMagnitudes table
        estacion_magnitud = EstacionesMagnitudes(ID_ESTACION=id_estacion, ID_MAGNITUD=magnitud)
        estacion_magnitud.save()
    
    dispositivo = Dispositivo(nombre, localizacion, estado, id_estacion, topics)
    dispositivo = dispositivo.save()
    
    # Add the estacion into the returning object
    estacion = Estacion.query.filter_by(ID_ESTACION=id_estacion).first()
    
    # Combine into single dict
    combined_dict = {**estacion.to_dict(), **dispositivo}
    
    # Get only the critical properties
    combined_dict = {key: combined_dict[key] for key in DISPOSITIVO_PROPERTIES}
    
    return jsonify(combined_dict), 201

def get_dispositivo(dispositivo_id):
    dispositivo = Dispositivo.get_dispositivo_by_id(dispositivo_id)
    if dispositivo:
        return jsonify(dispositivo), 200
    else:
        return jsonify({'error': 'Dispositivo not found'}), 404

def get_dispositivo_list():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    dispositivos = Dispositivo.get_dispositivos_by_pagination(page, per_page)
    # Get the estaciones for each dispositivo
    for dispositivo in dispositivos:
        id_estacion = dispositivo['id_estacion']
        estacion = Estacion.query.filter_by(ID_ESTACION=id_estacion).first()
        dispositivo['nombre_estacion'] = estacion.NOMBRE
        # Delete the topics property
        if 'topics' in dispositivo:
            del dispositivo['topics']
    return jsonify(dispositivos), 200

def get_dispositivo_by_id_estacion(id_estacion):
    dispositivo = Dispositivo.get_dispositivo_by_id_estacion(id_estacion)
    # Add estacion name to each dispositivo
    for disp in dispositivo:
        estacion = Estacion.query.filter_by(ID_ESTACION=id_estacion).first()
        disp['nombre_estacion'] = estacion.NOMBRE
    return jsonify(dispositivo), 200

def update_dispositivo(dispositivo_id):
    # ! FIX
    data = request.get_json()
    dispositivo = Dispositivo.get_dispositivo_by_id(dispositivo_id)
    if dispositivo:
        dispositivo = Dispositivo.update_dispositivo_by_id(dispositivo_id, data)
        return jsonify(dispositivo), 200
    else:
        return jsonify({'error': 'Dispositivo not found'}), 404

# You might also want to define a delete method for dispositivos, even though it wasn't explicitly requested:
def delete_dispositivo(dispositivo_id):
    # ! FIX
    dispositivo = Dispositivo.get_dispositivo_by_id(dispositivo_id)
    if dispositivo:
        dispositivo = Dispositivo.delete_dispositivo_by_id(dispositivo_id)
        return jsonify(dispositivo), 200
    else:
        return jsonify({'error': 'Dispositivo not found'}), 404
