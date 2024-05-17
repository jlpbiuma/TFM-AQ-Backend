# sensor_model.py
from api.database import mongo_db
from bson.objectid import ObjectId

class Sensor:
    def __init__(self, nombre, localizacion, estado, id_dispositivo):
        self.nombre = nombre
        self.localizacion = localizacion
        self.estado = estado
        self.id_dispositivo = id_dispositivo

    def save(self):
        sensors_collection = mongo_db['Sensor']
        result = sensors_collection.insert_one({
            'nombre': self.nombre,
            'localizacion': self.localizacion,
            'estado': self.estado,
            'id_dispositivo': self.id_dispositivo
        })
        return Sensor.get_sensor_by_id(result.inserted_id)

    @staticmethod
    def get_sensors_by_pagination(page, per_page):
        sensors_collection = mongo_db['Sensor']
        sensors_cursor = sensors_collection.find().skip((page - 1) * per_page).limit(per_page)
        sensors = []
        for sensor in sensors_cursor:
            sensor['_id'] = str(sensor['_id'])  # Convert ObjectId to string
            sensors.append(sensor)
        return sensors

    @staticmethod
    def get_sensor_by_id(id_sensor):
        sensors_collection = mongo_db['Sensor']
        sensor = sensors_collection.find_one({'_id': ObjectId(id_sensor)})
        if sensor:
            sensor['id_sensor'] = str(sensor['_id'])  # Convert ObjectId to string
            del sensor['_id']
        return sensor
    
    @staticmethod
    def get_sensors_by_id_dispositivo(id_dispositivo):
        sensors_collection = mongo_db['Sensor']
        sensors_cursor = sensors_collection.find({'id_dispositivo': str(id_dispositivo)})
        sensors = []  # List to hold all sensor documents
        for sensor in sensors_cursor:
            sensor['id_sensor'] = str(sensor['_id'])  # Convert ObjectId to string for JSON serialization
            del sensor['_id']  # Remove the original '_id' key
            sensors.append(sensor)
        return sensors


    @staticmethod
    def update_sensor_by_id(id_sensor, updated_data):
        sensors_collection = mongo_db['Sensor']
        sensors_collection.update_one({'_id': ObjectId(id_sensor)}, {'$set': updated_data})
        return Sensor.get_sensor_by_id(id_sensor)
    
    @staticmethod
    def delete_sensor_by_id(id_sensor):
        sensor_collectio = mongo_db['Sensor']
        sensor = Sensor.get_sensor_by_id(id_sensor)
        sensor_collectio.delete_one({'_id': ObjectId(id_sensor)})
        return sensor
