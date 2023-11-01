from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    text,
    Boolean
)

from database import engine, Base


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, index=True)
    price = Column(Integer, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))


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


Base.metadata.create_all(bind=engine)
