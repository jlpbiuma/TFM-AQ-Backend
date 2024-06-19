# models.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Magnitud(mysql_db.Model):
    __tablename__ = 'MAGNITUDES'
    ID_MAGNITUD: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    MAGNITUD: Mapped[str] = mapped_column(nullable=False)
    DESCRIPCION: Mapped[str] = mapped_column(nullable=False)
    ESCALA: Mapped[str] = mapped_column()

    def to_dict(self):
        return {
            'id_magnitud': self.ID_MAGNITUD,
            'magnitud': self.MAGNITUD,
            'descripcion': self.DESCRIPCION,
            'escala': self.ESCALA
        }

    def save(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self