import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Configuración de la conexión a la base de datos
MYSQL_CONFIG = {
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_ROOT_PASSWORD'),
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'database': os.environ.get('MYSQL_DATABASE')
}

def connection_mysql():
    try:
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        print("Conexión exitosa a la base de datos MySQL")
        return mysql_conn, mysql_cursor
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error en el nombre de usuario o contraseña de MySQL")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos MySQL no existe")
        else:
            print(err)
        return None, None
# Conexión a la base de datos MySQL
mysql_conn = None
mysql_cursor = None

while mysql_conn is None:
    mysql_conn, mysql_cursor = connection_mysql()
    if mysql_conn is None:
        print("Reintentando conexión en 5 segundos...")
        time.sleep(5)

# Función para insertar datos en la tabla ESTACIONES
def insert_estacion(id_administrador, nombre, localizacion):
    add_estacion = ("INSERT INTO ESTACIONES "
                    "(ID_ADMINISTRADOR, NOMBRE, LOCALIZACION) "
                    "VALUES (%s, %s, %s)")
    data_estacion = (id_administrador, nombre, localizacion)
    mysql_cursor.execute(add_estacion, data_estacion)
    mysql_conn.commit()

# Función para insertar datos en la tabla POSIBLES_MAGNITUDES
def insert_posibles_magnitudes(magnitud, descripcion, escala):
    add_magnitud = ("INSERT INTO POSIBLES_MAGNITUDES "
                    "(MAGNITUD, DESCRIPCION, ESCALA) "
                    "VALUES (%s, %s, %s)")
    data_magnitud = (magnitud, descripcion, escala)
    mysql_cursor.execute(add_magnitud, data_magnitud)
    mysql_conn.commit()
    # Return the ID of the inserted row
    return mysql_cursor.lastrowid

def insert_magnitud(id_magnitud):
    add_magnitud = ("INSERT INTO MAGNITUDES "
                    "(ID_POSIBLE_MAGNITUD) "
                    "VALUES (%s)")
    data_magnitud = (id_magnitud,)  # Note the comma after id_magnitud
    mysql_cursor.execute(add_magnitud, data_magnitud)
    mysql_conn.commit()


# Función para insertar datos en la tabla MEDIDAS
def insert_medida(id_magnitud, id_estacion, valor, fecha_hora):
    add_medida = ("INSERT INTO MEDIDAS "
                    "(ID_MAGNITUD, ID_ESTACION, VALOR, FECHA_HORA) "
                    "VALUES (%s, %s, %s, %s)")
    data_medida = (id_magnitud, id_estacion, valor, fecha_hora)
    mysql_cursor.execute(add_medida, data_medida)
    mysql_conn.commit()

def insert_estaciones_usuarios(id_estacion, id_usuario):
    # Check if the combination already exists
    check_query = ("SELECT * FROM ESTACIONES_USUARIOS "
                   "WHERE ID_ESTACION = %s AND ID_USUARIO = %s")
    check_data = (id_estacion, id_usuario)
    mysql_cursor.execute(check_query, check_data)
    if mysql_cursor.fetchone():
        print("Combination already exists. Skipping insertion.")
        return
    
    # If combination doesn't exist, proceed with insertion
    add_estacion_usuario = ("INSERT INTO ESTACIONES_USUARIOS "
                            "(ID_ESTACION, ID_USUARIO) "
                            "VALUES (%s, %s)")
    data_estacion_usuario = (id_estacion, id_usuario)
    try:
        mysql_cursor.execute(add_estacion_usuario, data_estacion_usuario)
    except:
        return
    mysql_conn.commit()

def insert_estaciones_dispositivos(id_estacion, id_dispositivo):
    # Check if the combination already exists
    check_query = ("SELECT * FROM ESTACIONES_DISPOSITIVOS "
                   "WHERE ID_ESTACION = %s AND ID_DISPOSITIVO = %s")
    check_data = (id_estacion, id_dispositivo)
    mysql_cursor.execute(check_query, check_data)
    if mysql_cursor.fetchone():
        print("Combination already exists. Skipping insertion.")
        return
    
    # If combination doesn't exist, proceed with insertion
    add_estacion_dispositivo = ("INSERT INTO ESTACIONES_DISPOSITIVOS "
                                "(ID_ESTACION, ID_DISPOSITIVO) "
                                "VALUES (%s, %s)")
    data_estacion_dispositivo = (id_estacion, id_dispositivo)
    try:
        mysql_cursor.execute(add_estacion_dispositivo, data_estacion_dispositivo)
    except:
        return 
    mysql_conn.commit()
