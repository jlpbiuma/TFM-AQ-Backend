import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import json

def create_encoded_key(password):
    return (password + 'my_secret_backend_key').encode()

def encrypt_data(data, password):
    # Generate a random salt
    salt = os.urandom(16)
    
    # Derive a key from the password using Scrypt KDF
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    # Create unique password for this backend
    encoded_key = create_encoded_key(password)
    
    key = kdf.derive(encoded_key)

    # Generate a random IV (Initialization Vector)
    iv = os.urandom(12)
    
    # Encrypt the data using AES-GCM
    aesgcm = AESGCM(key)
    encrypted_data = aesgcm.encrypt(iv, data.encode(), None)
    
    # Return the salt, iv, and encrypted data
    return base64.b64encode(salt + iv + encrypted_data).decode()

def decrypt_data(encrypted_data, password):
    # Decode the base64 encoded data
    encrypted_data = base64.b64decode(encrypted_data)
    
    # Extract the salt, iv, and actual encrypted data
    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    actual_encrypted_data = encrypted_data[28:]
    
    # Derive the same key from the password using Scrypt KDF
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    # Create unique password for this backend
    encoded_key = create_encoded_key(password)
    
    key = kdf.derive(encoded_key)
    
    # Decrypt the data using AES-GCM
    aesgcm = AESGCM(key)
    decrypted_data = aesgcm.decrypt(iv, actual_encrypted_data, None)
    
    return decrypted_data.decode()

# Example usage
data = json.dumps({
    "ID_UNIDADES": [1],
    "ID_DISPOSITIVO": 1
})

password = "1234"

# Encrypt the data
encrypted_data = encrypt_data(data, password)
print(f"Encrypted Data: {encrypted_data}")

bad_password = "3527" 

# Decrypt the data
decrypted_data = decrypt_data(encrypted_data, bad_password)
print(f"Decrypted Data: {decrypted_data}")
