from sqlalchemy.orm import declarative_base
from sqlalchemy import (Column,
                        Integer, String, DateTime, func, Index)

Base = declarative_base()


class Key(Base):
    __tablename__ = 'key'
    id = Column(Integer, primary_key=True)
    access_url = Column(String, nullable=False)
    user = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, server_default=func.now())
    expiration_date = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index('idx_key', 'access_url'),
        Index('idx_user', 'user'),
        Index('idx_expiration', 'expiration_date'),
    )