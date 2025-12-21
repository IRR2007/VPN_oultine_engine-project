from sqlalchemy.orm import declarative_base
from sqlalchemy import (Column,
                        Integer, String, Date, func, Index)

Base = declarative_base()


class Key(Base):
    __tablename__ = 'key'
    id = Column(Integer, primary_key=True)
    outline_id = Column(String, nullable=False)
    access_url = Column(String, nullable=False)
    user = Column(String, nullable=False)
    creation_date = Column(Date, nullable=False, server_default=func.now())
    expiration_date = Column(Date, nullable=False)

    __table_args__ = (
        Index('idx_key', 'access_url'),
        Index('idx_user', 'user'),
        Index('idx_expiration', 'expiration_date'),
    )