import hashlib
import os

def get_hashed_password(password):
    hashed_password = hashlib.sha256((password + os.environ.get('SECRET_KEY')).encode()).hexdigest()
    return hashed_password