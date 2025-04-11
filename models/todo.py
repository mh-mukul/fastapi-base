from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean

from models.abstract import AbstractBase


class Todo(AbstractBase):
    __tablename__ = "todos"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"{self.id}"

    @classmethod
    def get_active(cls, db: Session):
        return db.query(cls).filter(cls.is_deleted == False)
