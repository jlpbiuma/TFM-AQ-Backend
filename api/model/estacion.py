from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Estacion(mysql_db.Model):
    __tablename__ = 'ESTACIONES'
    ID_ESTACION: Mapped[int] = mapped_column(primary_key=True)
    ID_ADMINISTRADOR: Mapped[str]
    IP_GATEWAY: Mapped[str]
    IP_LOCAL: Mapped[str]
    NOMBRE: Mapped[str]
    LOCALIZACION: Mapped[str]
    FECHA_HORA_IP: Mapped[str]
    
    def to_dict(self):
        return {
            'id': self.ID_ESTACION,
            'id_administrador': self.ID_ADMINISTRADOR,
            'nombre': self.NOMBRE,
            'ip_gateway': self.IP_GATEWAY,
            'localizacion': self.LOCALIZACION,
            'fecha_hora_ip': self.FECHA_HORA_IP,
            'ip_local': self.IP_LOCAL
        }
