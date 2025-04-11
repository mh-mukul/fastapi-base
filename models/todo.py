from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from config.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_completed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(6), default=datetime.now)
    updated_at = Column(DateTime(6), default=datetime.now)

    def __repr__(self):
        return f"{self.id}"
