# models.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Magnitud(mysql_db.Model):
    __tablename__ = 'POSIBLES_MAGNITUDES'
    ID_MAGNITUD: Mapped[int] = mapped_column(primary_key=True)
    MAGNITUD: Mapped[str]
    DESCRIPCION: Mapped[str]
    ESCALA: Mapped[str]
    
    def to_dict(self):
        return {
            'id': self.ID_MAGNITUD,
            'magnitud': self.MAGNITUD,
            'descripcion': self.DESCRIPCION,
            'escala': self.ESCALA
        }
