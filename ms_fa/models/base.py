import datetime
import uuid
from typing import List, Any
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import declared_attr
from ms_fa.db import Base


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            default=datetime.datetime.utcnow,
            server_default=func.now(),
            nullable=False
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=datetime.datetime.utcnow,
            server_default=func.now(),
            onupdate=datetime.datetime.utcnow,
            nullable=False
        )


class Model(Base, TimestampMixin):
    __abstract__ = True

    _fillable: List[str] = []

    def __init__(self, data: dict = None, **kwargs):
        super().__init__(**kwargs)
        if data is not None:
            self.set_attrs(data)

    def __repr__(self):
        return f"<{self.__tablename__} id={self.id}>"

    def set_attrs(self, data: dict) -> None:
        for attr, value in data.items():
            if attr in self._fillable:
                setattr(self, attr, value)

    def update(self, data: dict) -> None:
        self.set_attrs(data)

