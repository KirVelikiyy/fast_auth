from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session
from database.database import Base


class Model(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    def add_to_db(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
