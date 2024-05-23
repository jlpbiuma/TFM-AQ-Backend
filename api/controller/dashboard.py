from api.database import mysql_db

def get_dashboard_by_id_estacion(id_estacion):
    query = '''
    SELECT c.VALOR
    FROM ESTACIONES
    
    '''