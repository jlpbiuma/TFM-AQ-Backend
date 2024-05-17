# user_model.py
from api.database import mongo_db
from bson.objectid import ObjectId

class Usuario:
    def __init__(self, username, email, name, password, role=1):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.name = name

    def save(self):
        users_collection = mongo_db['Usuario']
        result = users_collection.insert_one({
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'role': self.role
        })
        return Usuario.get_user_by_id(result.inserted_id)

    @staticmethod
    def get_users_by_pagination(page, per_page):
        users_collection = mongo_db['Usuario']
        users_cursor = users_collection.find().skip((page - 1) * per_page).limit(per_page)
        users = []
        for user in users_cursor:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
            users.append(user)
        return users

    @staticmethod
    def get_user_by_id(id_usuario):
        users_collection = mongo_db['Usuario']
        user = users_collection.find_one({'_id': ObjectId(id_usuario)})
        if user:
            user['id_usuario'] = str(user['_id'])  # Convert ObjectId to string
            del user['_id']
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
        users_collection.update_one({'_id': ObjectId(id_usuario)}, {'$set': updated_data})
        return Usuario.get_user_by_id(id_usuario)

    @staticmethod
    def delete_user_by_id(id_usuario):
        users_collection = mongo_db['Usuario']
        user = Usuario.get_user_by_id(id_usuario)
        users_collection.delete_one({'_id': ObjectId(id_usuario)})
        return user

