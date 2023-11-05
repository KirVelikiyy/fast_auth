from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    text,
    Boolean
)

from database import engine, Base
from utils.jwt import get_password_hash


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(60), nullable=True, unique=True)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        hashed_password = self.hash_password(password)
        kwargs.update({"hashed_password": hashed_password})

        super(User, self).__init__(**kwargs)

    @staticmethod
    def hash_password(password: str) -> str:
        return get_password_hash(password)


Base.metadata.create_all(bind=engine)
