from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Unidad(mysql_db.Model):
    __tablename__ = 'UNIDADES'
    ID_UNIDAD: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_MAGNITUD: Mapped[int] = mapped_column(ForeignKey('POSIBLES_MAGNITUDES.ID_MAGNITUD'), nullable=False)
    ID_ESTACION: Mapped[int] = mapped_column(ForeignKey('ESTACIONES.ID_ESTACION'), nullable=False)
    
    def to_dict(self):
        return {
            'id_unidad': self.ID_UNIDAD,
            'id_magnitud': self.ID_MAGNITUD,
            'id_estacion': self.ID_ESTACION
        }
