from sqlalchemy import Column, Integer
from database.database import Base


class Model(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
