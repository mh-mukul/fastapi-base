from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean

from config.database import Base


class AbstractBase(Base):
    __abstract__ = True

    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(6), default=datetime.now)
    updated_at = Column(DateTime(6), default=datetime.now)
