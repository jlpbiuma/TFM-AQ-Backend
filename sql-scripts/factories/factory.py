import random
from dotenv import load_dotenv
from functions import *
import random
from datetime import datetime, timedelta


# ! ESTE SCRIPT SIRVE PARA INTRODUCIR VALORES EN LA BASE DE DATOS DE FORMA SINTÉTICA

N_ESTACIONES = 5
N_USUARIOS = 50
N_DISPOSITIVOS = 20
N_SENSORES = 40
N_MEDIDAS = 100
MAGNITUDES = [
    ('Temperatura', 'Temperatura del aire', 'Celsius'),
    ('Humedad', 'Humedad relativa', '%'),
    ('Presión', 'Presión atmosférica', 'hPa')
]

# Generar y vincular datos de ejemplo
def generate_and_link_data(n_medidas, estaciones_range, magnitudes, usuarios_range, dispositivos_range, sensores_range):
    # Generar datos de ejemplo
    # Insertar estaciones
    for i in range(*estaciones_range):
        insert_estacion(random.randint(1, 10), f'Estacion_{i}', f'Localizacion_{i}')
    
    # Insertar posibles magnitudes
    for magnitud in magnitudes:
        insert_magnitud(*magnitud)
    
    # Insertar medidas
    for i in range(*estaciones_range):
        for j in range(1, len(magnitudes) + 1):
            for k in range(1, n_medidas):
                fecha_hora = datetime.now() - timedelta(seconds=random.randint(0, 60))
                insert_medida(j, i, random.uniform(0, 100), fecha_hora)

    # Insertar usuarios en MongoDB y vincular con estaciones en MySQL
    for i in range(*usuarios_range):
        username = f'usuario{i}'
        email = f'usuario{i}@ejemplo.com'
        nombre = f'Nombre {i}'
        password = 'password123'
        id_usuario_mongo = insert_mongo_user(username, email, nombre, password)
        
        id_estacion_sql = random.randint(*estaciones_range)  # Suponiendo que las estaciones SQL ya existen
        insert_estaciones_usuarios(id_estacion_sql, id_usuario_mongo)
    
    # Insertar dispositivos en MongoDB y vincular con estaciones en MySQL
    for i in range(*dispositivos_range):
        nombre = f'dispositivo{i}'
        localizacion = f'Localizacion {i}'
        estado = 'activo'
        id_dispositivo_mongo = insert_mongo_dispositivo(nombre, localizacion, estado)
        
        id_estacion_sql = random.randint(*estaciones_range)  # Suponiendo que las estaciones SQL ya existen
        insert_estaciones_dispositivos(id_estacion_sql, id_dispositivo_mongo)
    
    # Insertar sensores en MongoDB
    for i in range(*sensores_range):
        nombre = f'sensor{i}'
        id_medidas = [f'medida{j}' for j in range(1, len(magnitudes))]  # Iterar sobre el número de magnitudes
        id_dispositivo = insert_mongo_dispositivo(f'dispositivo{i}', f'Localizacion {i}', 'activo')
        localizacion = f'Localizacion {i}'
        insert_mongo_sensor(nombre, id_medidas, id_dispositivo, localizacion)

# Llamar a la función con los parámetros deseados
generate_and_link_data(
    n_medidas=N_MEDIDAS + 1,
    estaciones_range=(1, N_ESTACIONES + 1),
    magnitudes=MAGNITUDES,
    usuarios_range=(1, N_USUARIOS + 1),
    dispositivos_range=(1, N_DISPOSITIVOS + 1),
    sensores_range=(1, N_SENSORES + 1)
)

# Cerrar la conexión a las bases de datos
mysql_cursor.close()
mysql_conn.close()
mongo_client.close()
print("Datos insertados y conexiones cerradas")
