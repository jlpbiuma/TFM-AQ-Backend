# models.py
from api.database import mysql_db

class Estacion(mysql_db.Model):
    __tablename__ = 'ESTACIONES'

    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    id_administrador = mysql_db.Column(mysql_db.Integer)
    nombre = mysql_db.Column(mysql_db.String(50))
    localizacion = mysql_db.Column(mysql_db.String(100))

    def __repr__(self):
        return f'<Estacion {self.nombre}>'
