from sqlalchemy import Column, Integer
from database import Base


class Model(Base):
    id = Column(Integer, primary_key=True)
