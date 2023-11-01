from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    text,
)

from database import engine, Base


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, index=True)
    price = Column(Integer, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('Now()'))


Base.metadata.create_all(bind=engine)
