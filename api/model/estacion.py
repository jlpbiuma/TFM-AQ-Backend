# models.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Estacion(mysql_db.Model):
    __tablename__ = 'ESTACIONES'
    ID_ESTACION: Mapped[int] = mapped_column(primary_key=True)
    ID_ADMINISTRADOR: Mapped[str]
    NOMBRE: Mapped[str]
    LOCALIZACION: Mapped[str]
    
    def to_dict(self):
        return {
            'id': self.ID_ESTACION,
            'id_administrador': self.ID_ADMINISTRADOR,
            'nombre': self.NOMBRE,
            'localizacion': self.LOCALIZACION
        }
