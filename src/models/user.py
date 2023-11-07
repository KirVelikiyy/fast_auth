from sqlalchemy import Column, String, TIMESTAMP, Boolean, text
from sqlalchemy.orm import relationship, Mapped

from utils.jwt import TokenManager
from .base import Model
from .session import AuthSession


class User(Model):
    __tablename__ = 'users'
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(60), nullable=True, unique=True)
    first_name = Column(String(20), nullable=True)
    last_name = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))
    auth_sessions: Mapped[list["AuthSession"]] = relationship()

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        hashed_password = self.hash_password(password)
        kwargs.update({"hashed_password": hashed_password})

        super(User, self).__init__(**kwargs)

    @staticmethod
    def hash_password(password: str) -> str:
        return TokenManager.get_password_hash(password)
