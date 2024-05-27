# user_model.py
from api.database import mongo_db
from bson.objectid import ObjectId
from api.controller.tools import *

class Usuario:
    def __init__(self, username, email, name, password, role=1):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.name = name

    def save(self):
        # Hash the password before saving
        hashed_password = get_hashed_password(self.password)
        users_collection = mongo_db['Usuario']
        result = users_collection.insert_one({
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'password': hashed_password,  # Save hashed password
            'role': self.role or 1
        })
        return Usuario.get_user_by_id(result.inserted_id)

    @staticmethod
    def get_users_by_pagination(page, per_page):
        # ! BASURA, NO USAR
        users_collection = mongo_db['Usuario']
        users_cursor = users_collection.find().skip((page - 1) * per_page).limit(per_page)
        users = []
        for user in users_cursor:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
            del user['password']
            users.append(user)
        return users

    @staticmethod
    def get_user_by_id(id_usuario):
        users_collection = mongo_db['Usuario']
        user = users_collection.find_one({'_id': ObjectId(id_usuario)})
        if user:
            user['id_usuario'] = str(user['_id'])  # Convert ObjectId to string
            del user['_id']
            del user['password']
        return user
    
    @staticmethod
    def get_user_by_username(username):
        users_collection = mongo_db['Usuario']
        user = users_collection.find_one({'username': username})
        if user:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return user

    @staticmethod
    def get_role_by_username(username):
        users_collection = mongo_db['Usuario']
        user = users_collection.find_one({'username': username})
        if user:
            rol = int(user['role'])  # Convert ObjectId to string
        return rol

    @staticmethod
    def get_user_by_email(email):
        users_collection = mongo_db['Usuario']
        user = users_collection.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return user

    @staticmethod
    def get_role_by_id(id_usuario):
        user = Usuario.get_user_by_id(id_usuario)
        if user:
            return user.get('role')
        else:
            return None

    @staticmethod
    def update_user_by_id(id_usuario, updated_data):
        users_collection = mongo_db['Usuario']
        # Ensure the _id key is not in the updated_data dictionary
        if '_id' in updated_data or 'id_usuario' in updated_data:
            del updated_data['_id']
            del updated_data['id_usuario']
        if 'password' in updated_data:
            updated_data['password'] = get_hashed_password(updated_data['password'])
        users_collection.update_one({'_id': ObjectId(id_usuario)}, {'$set': updated_data})
        return Usuario.get_user_by_id(id_usuario)


    @staticmethod
    def delete_user_by_id(id_usuario):
        users_collection = mongo_db['Usuario']
        user = Usuario.get_user_by_id(id_usuario)
        users_collection.delete_one({'_id': ObjectId(id_usuario)})
        return user
    
    @staticmethod
    def authenticate(username, password):
        users_collection = mongo_db['Usuario']
        user = users_collection.find_one({'username': username})
        if user:
            # Hash the provided password using the same method used during registration
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Check if the hashed password matches the stored hashed password
            if user['password'] == hashed_password:
                user['id_usuario'] = str(user['_id'])  # Convert ObjectId to string
                return user
        return None