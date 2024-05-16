import os
from pymongo import MongoClient

def setup_mongo_connection():
    try:
        mongo_host = os.environ.get('MONGO_HOST', 'localhost')
        mongo_port = os.environ.get('MONGO_PORT', 27017)
        mongo_user = os.environ.get('MONGO_USER', 'root')
        mongo_password = os.environ.get('MONGO_PASSWORD', 'password')
        mongo_database = os.environ.get('MONGO_DATABASE', 'AQ')
        # Construct MongoDB URI
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_database}"
        client = MongoClient(mongo_uri)
        return client[mongo_database]
    except KeyError as e:
        raise RuntimeError(f"Environment variable {e} is not set. Make sure all required environment variables are set.")
