from sqlalchemy import Column, Integer
from database.database import Base


class Model(Base):
    id = Column(Integer, primary_key=True)
