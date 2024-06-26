import mysql.connector
from mysql.connector import errorcode
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random
import hashlib

def get_hashed_password(password):
    hashed_password = hashlib.sha256((password + os.environ.get('SECRET_KEY')).encode()).hexdigest()
    return hashed_password


load_dotenv()

mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))  # Convert port to int
mongo_user = os.environ.get('MONGO_USER', 'root')
mongo_password = os.environ.get('MONGO_PASSWORD', 'password')
# Configuración de la conexión a la base de datos MongoDB
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
# mongo_uri = os.environ.get('MONGO_ATLAS_URI', '')
mongo_client = MongoClient(mongo_uri)
MONGO_DB = mongo_client[os.getenv('MONGO_DATABASE')]

# Función para insertar datos en la colección de MongoDB
def insert_mongo_user(username, email, nombre, password):
    user_collection = MONGO_DB['Usuario']
    random_role = random.choice([1, 2, 3, 4])
    user_id = user_collection.insert_one({
        'username': username,
        'email': email,
        'name': nombre,
        'visible_password': password,
        'password': get_hashed_password(password),
        'role': random_role,
        'phone': ''.join(random.choices('0123456789', k=9))
    }).inserted_id
    return str(user_id)

def insert_mongo_dispositivo(nombre, localizacion, estado, estaciones):
    dispositivo_collection = MONGO_DB['Dispositivo']
    random_id_estacion = random.choice(estaciones)
    dispositivo_id = dispositivo_collection.insert_one({
        'name': nombre,
        'location': localizacion,
        'state': estado,
        'id_estacion': random_id_estacion
    }).inserted_id
    return str(dispositivo_id)