from flask import request
from time import time

def create_medida():
    if request.method == 'POST':
        data = request.json
        timestamp = time()
        if data:
            print("Received message:", data)
            print("Timestamp:", timestamp)
            # Here you can process the received data further
            # For example, you can save it to a database, perform calculations, etc.
            return "Message received successfully", 200
        else:
            return "No data received", 400
    else:
        return "Method not allowed", 405
