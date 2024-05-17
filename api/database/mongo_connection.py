# database.py
import os
from pymongo import MongoClient

mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_port = int(os.environ.get('MONGO_PORT', 27017))  # Convert port to int
mongo_user = os.environ.get('MONGO_USER', 'root')
mongo_password = os.environ.get('MONGO_PASSWORD', 'password')
mongo_database = os.environ.get('MONGO_DATABASE', 'AQ')
# Construct MongoDB URI
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client[mongo_database]