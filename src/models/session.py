from sqlalchemy import Column, String, ForeignKey
from .base import Model


class AuthSession(Model):
    __tablename__ = 'auth_sessions'
    user_id = Column(ForeignKey("users.id"))
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
