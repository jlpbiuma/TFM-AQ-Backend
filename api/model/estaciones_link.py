from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class EstacionesUsuarios(mysql_db.Model):
    __tablename__ = 'ESTACIONES_USUARIOS'
    ID_ESTACION: Mapped[int] = mapped_column(ForeignKey('ESTACIONES.ID_ESTACION'), primary_key=True)
    ID_USUARIO: Mapped[str] = mapped_column(String, primary_key=True)
    
    def to_dict(self):
        return {
            'id_estacion': self.ID_ESTACION,
            'id_usuario': self.ID_USUARIO,
        }

class EstacionesDispositivos(mysql_db.Model):
    __tablename__ = 'ESTACIONES_DISPOSITIVOS'
    ID_ESTACION: Mapped[int] = mapped_column(ForeignKey('ESTACIONES.ID_ESTACION'), primary_key=True, nullable=False)
    ID_DISPOSITIVO: Mapped[str] = mapped_column(String, nullable=False)
    
    def to_dict(self):
        return {
            'id_estacion': self.ID_ESTACION,
            'id_dispositivo': self.ID_DISPOSITIVO,
        }