import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declared_attr


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

