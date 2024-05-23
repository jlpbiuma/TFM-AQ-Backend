import hashlib

def get_hashed_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password