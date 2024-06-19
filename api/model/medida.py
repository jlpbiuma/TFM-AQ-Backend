from sqlalchemy import Integer, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Medida(mysql_db.Model):
    __tablename__ = 'MEDIDAS'
    ID_MEDIDA: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_MAGNITUD: Mapped[int] = mapped_column(ForeignKey('MAGNITUDES.ID_MAGNITUD'), nullable=False)
    ID_ESTACION: Mapped[int] = mapped_column(ForeignKey('ESTACIONES.ID_ESTACION'), nullable=False)
    VALOR: Mapped[float] = mapped_column(Float, nullable=False)
    FECHA_HORA: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    
    def to_dict(self):
        return {
            'id_medida': self.ID_MEDIDA,
            'id_magnitud': self.ID_MAGNITUD,
            'valor': self.VALOR,
            'fecha_hora': self.FECHA_HORA
        }
