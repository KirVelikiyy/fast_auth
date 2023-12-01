from sqlalchemy import Column, String, ForeignKey
from .base import Model


class AuthSession(Model):
    __tablename__ = 'auth_sessions'
    username = Column(ForeignKey("users.username"))
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
