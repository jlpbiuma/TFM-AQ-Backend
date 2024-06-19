from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.database import mysql_db

class Logs(mysql_db.Model):
    __tablename__ = 'LOGS'
    ID_LOG: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ENDPOINT: Mapped[str] = mapped_column(nullable=False)
    METHOD: Mapped[str] = mapped_column(nullable=False)
    STATUS_CODE: Mapped[int] = mapped_column(nullable=False)
    IP_ADDRESS: Mapped[str] = mapped_column()
    TIMESTAMP: Mapped[str] = mapped_column()
    REQUEST_BODY: Mapped[str] = mapped_column()
    RESPONSE_BODY: Mapped[str] = mapped_column()

    def to_dict(self):
        return {
            'id_log': self.ID_LOG,
            'endpoint': self.ENDPOINT,
            'method': self.METHOD,
            'status_code': self.STATUS_CODE,
            'ip_address': self.IP_ADDRESS,
            'timestamp': self.TIMESTAMP,
            'request_body': self.REQUEST_BODY,
            'response_body': self.RESPONSE_BODY
        }

    def save(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self