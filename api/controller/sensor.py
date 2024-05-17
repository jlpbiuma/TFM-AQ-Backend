from flask import jsonify, request
from api.model import Sensor

def create_sensor():
    data = request.get_json()
    nombre = data.get('nombre')
    localizacion = data.get('localizacion')
    estado = data.get('estado')
    id_dispositivo = data.get('id_dispositivo')

    if not nombre or not localizacion or not estado or not id_dispositivo:
        return jsonify({'error': 'Nombre, localizacion, estado, and id_dispositivo are required'}), 400

    sensor = Sensor(nombre, localizacion, estado, id_dispositivo)
    sensor = sensor.save()
    return jsonify(sensor), 201

def get_sensor(sensor_id):
    sensor = Sensor.get_sensor_by_id(sensor_id)
    if sensor:
        return jsonify(sensor), 200
    else:
        return jsonify({'error': 'Sensor not found'}), 404

def get_sensor_list():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    sensors = Sensor.get_sensors_by_pagination(page, per_page)
    return jsonify(sensors), 200

def get_sensors_by_dispositivo(id_dispositivo):
    sensors = Sensor.get_sensors_by_id_dispositivo(id_dispositivo)
    return jsonify(sensors), 200

def update_sensor(sensor_id):
    data = request.get_json()
    sensor = Sensor.get_sensor_by_id(sensor_id)
    if sensor:
        sensor = Sensor.update_sensor_by_id(sensor_id, data)
        return jsonify(sensor), 200
    else:
        return jsonify({'error': 'Sensor not found'}), 404

def delete_sensor(sensor_id):
    sensor = Sensor.get_sensor_by_id(sensor_id)
    if sensor:
        sensor = Sensor.delete_sensor_by_id(sensor_id)
        return jsonify(sensor), 200
    else:
        return jsonify({'error': 'Sensor not found'}), 404
