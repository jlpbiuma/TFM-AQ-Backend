# models.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class PosiblesMagnitudes(mysql_db.Model):
    __tablename__ = 'POSIBLES_MAGNITUDES'
    ID_POSIBLE_MAGNITUD: Mapped[int] = mapped_column(primary_key=True)
    MAGNITUD: Mapped[str]
    DESCRIPCION: Mapped[str]
    ESCALA: Mapped[str]
    
    def to_dict(self):
        return {
            'id_posible_magnitud': self.ID_POSIBLE_MAGNITUD,
            'magnitud': self.MAGNITUD,
            'descripcion': self.DESCRIPCION,
            'escala': self.ESCALA
        }
        
class Magnitud(mysql_db.Model):
    __tablename__ = 'MAGNITUDES'
    ID_MAGNITUD: Mapped[int] = mapped_column(primary_key=True)
    ID_POSIBLE_MAGNITUD: Mapped[int] = mapped_column(ForeignKey('POSIBLES_MAGNITUDES.ID_POSIBLE_MAGNITUD'))
    
    def to_dict(self):
        return {
            'id_magnitud': self.ID_MAGNITUD,
            'id_posible_magnitud': self.ID_POSIBLE_MAGNITUD,
        }
        

