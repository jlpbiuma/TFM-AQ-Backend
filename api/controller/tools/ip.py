from cryptography.fernet import Fernet
import os
import base64

# Get the SECRET_KEY from environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")

def encrypt_ip(public_ip):
    return public_ip
    fernet = Fernet(SECRET_KEY.encode())
    encrypted_ip = fernet.encrypt(public_ip.encode())
    return encrypted_ip.decode()

def decrypt_ip(encrypted_ip):
    return encrypted_ip
    fernet = Fernet(SECRET_KEY.encode())
    decrypted_ip = fernet.decrypt(encrypted_ip.encode())
    return decrypted_ip.decode()

def decrypt_estacion_ip(estacion_dict):
    return estacion_dict
    decrypted_ip = decrypt_ip(estacion_dict['IP_GATEWAY'])
    estacion_dict['IP_GATEWAY'] = decrypted_ip
    return estacion_dict
