from sqlalchemy import Integer, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Medida(mysql_db.Model):
    __tablename__ = 'MEDIDAS'
    ID_MEDIDA: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ID_UNIDAD: Mapped[int] = mapped_column(ForeignKey('UNIDADES.ID_UNIDAD'), nullable=False)
    VALOR: Mapped[float] = mapped_column(Float, nullable=False)
    FECHA_HORA: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    
    def to_dict(self):
        return {
            'id_medida': self.ID_MEDIDA,
            'id_unidad': self.ID_UNIDAD,
            'valor': self.VALOR,
            'fecha_hora': self.FECHA_HORA
        }
