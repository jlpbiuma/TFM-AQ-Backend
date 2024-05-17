# dispositivo_model.py
from api.database import mongo_db
from bson.objectid import ObjectId

class Dispositivo:
    def __init__(self, nombre, localizacion, estado, id_estacion):
        self.nombre = nombre
        self.localizacion = localizacion
        self.estado = estado
        self.id_estacion = id_estacion

    def save(self):
        dispositivos_collection = mongo_db['Dispositivo']
        result = dispositivos_collection.insert_one({
            'nombre': self.nombre,
            'localizacion': self.localizacion,
            'estado': self.estado,
            'id_estacion': self.id_estacion
        })
        return Dispositivo.get_dispositivo_by_id(result.inserted_id)

    @staticmethod
    def get_dispositivos_by_pagination(page, per_page):
        dispositivos_collection = mongo_db['Dispositivo']
        dispositivos_cursor = dispositivos_collection.find().skip((page - 1) * per_page).limit(per_page)
        dispositivos = []
        for dispositivo in dispositivos_cursor:
            dispositivo['_id'] = str(dispositivo['_id'])  # Convert ObjectId to string
            dispositivos.append(dispositivo)
        return dispositivos

    @staticmethod
    def get_dispositivo_by_id(id_dispositivo):
        dispositivos_collection = mongo_db['Dispositivo']
        dispositivo = dispositivos_collection.find_one({'_id': ObjectId(id_dispositivo)})
        if dispositivo:
            dispositivo['id_dispositivo'] = str(dispositivo['_id'])  # Convert ObjectId to string
            del dispositivo['_id']
        return dispositivo
    
    @staticmethod
    def get_dispositivo_by_id_estacion(id_estacion):
        dispositivo_collection = mongo_db['Dispositivo']
        dispositivo_cursor = dispositivo_collection.find({'id_estacion': int(id_estacion)})
        dispositivos = []  # List to hold all sensor documents
        for dispositivo in dispositivo_cursor:
            dispositivo['id_dispositivo'] = str(dispositivo['_id'])  # Convert ObjectId to string for JSON serialization
            del dispositivo['_id']  # Remove the original '_id' key
            dispositivos.append(dispositivo)
        return dispositivos

    @staticmethod
    def update_dispositivo_by_id(id_dispositivo, updated_data):
        dispositivos_collection = mongo_db['Dispositivo']
        dispositivos_collection.update_one({'_id': ObjectId(id_dispositivo)}, {'$set': updated_data})
        return Dispositivo.get_dispositivo_by_id(id_dispositivo)
    
    @staticmethod
    def delete_dispositivo_by_id(id_dispositivo):
        dispositivo_collectio = mongo_db['Dispositivo']
        dispositivo = Dispositivo.get_dispositivo_by_id(id_dispositivo)
        dispositivo_collectio.delete_one({'_id': ObjectId(id_dispositivo)})
        return dispositivo
