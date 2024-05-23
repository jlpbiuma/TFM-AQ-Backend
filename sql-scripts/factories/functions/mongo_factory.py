import mysql.connector
from mysql.connector import errorcode
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))  # Convert port to int
mongo_user = os.environ.get('MONGO_USER', 'root')
mongo_password = os.environ.get('MONGO_PASSWORD', 'password')
# Configuración de la conexión a la base de datos MongoDB
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
mongo_client = MongoClient(mongo_uri)
MONGO_DB = mongo_client[os.getenv('MONGO_DATABASE')]

# Función para insertar datos en la colección de MongoDB
def insert_mongo_user(username, email, nombre, password):
    user_collection = MONGO_DB['Usuario']
    user_id = user_collection.insert_one({
        'username': username,
        'email': email,
        'nombre': nombre,
        'password': password
    }).inserted_id
    return str(user_id)

def insert_mongo_dispositivo(nombre, localizacion, estado):
    dispositivo_collection = MONGO_DB['Dispositivo']
    dispositivo_id = dispositivo_collection.insert_one({
        'nombre': nombre,
        'localizacion': localizacion,
        'estado': estado
    }).inserted_id
    return str(dispositivo_id)

def insert_mongo_sensor(nombre, id_medidas, id_dispositivo, localizacion):
    sensor_collection = MONGO_DB['Sensor']
    sensor_id = sensor_collection.insert_one({
        'nombre': nombre,
        'id_medidas': id_medidas,
        'id_dispositivo': id_dispositivo,
        'localizacion': localizacion
    }).inserted_id
    return str(sensor_id)