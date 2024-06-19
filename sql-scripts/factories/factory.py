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
    ('Temperatura', 'Temperatura del aire', 'Absoluta'),
    ('Humedad', 'Humedad relativa', 'Relativa'),
    ('Monóxido de carbono', 'CO', 'Absoluta'),
    ('Dióxido de carbono', 'CO2', 'Absoluta'),
]

# Generar y vincular datos de ejemplo
def generate_and_link_data(n_medidas, estaciones_range, magnitudes, usuarios_range, dispositivos_range, sensores_range):
    # Generar datos de ejemplo
    # Insertar posibles magnitudes
    posibles_magnitudes = []
    ids_estaciones = []
    for magnitud in magnitudes:
        id_posible_magnitud = insert_posibles_magnitudes(*magnitud)
        posibles_magnitudes.append(id_posible_magnitud)
    # Insertar estaciones
    for i in range(*estaciones_range):
        id_administrador = random.randint(1, 10)
        nombre = f'Estacion_{i}'
        localizacion = f'Localizacion_{i}'
        ip_gateway = generate_random_ip()  # Generate random IP address
        ip_local = generate_random_local_ip()
        fecha_hora_ip = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        id_estacion = insert_estacion(id_administrador, nombre, localizacion, ip_gateway, ip_local, fecha_hora_ip)
        ids_estaciones.append(id_estacion)
    
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
        id_dispositivo_mongo = insert_mongo_dispositivo(nombre, localizacion, estado, ids_estaciones)
        
        id_estacion_sql = random.randint(*estaciones_range)  # Suponiendo que las estaciones SQL ya existen
        insert_estaciones_dispositivos(id_estacion_sql, id_dispositivo_mongo)
        
    # Insertar medidas
    # for i in range(*estaciones_range):
    #     for j in range(1, len(magnitudes) + 1):
    #         for k in range(1, n_medidas):
    #             fecha_hora = datetime.now() - timedelta(seconds=random.randint(0, 60))
                # insert_medida(j, i, random.uniform(0, 100), fecha_hora)

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
