import uuid
from sqlalchemy import Column, String, DateTime
from ms_fa.models.base import Model


class ResetPassword(Model):
    __tablename__ = 'reset_password'

    _fillable = [
        "token",
        "username",
        "expires_at",
    ]

    id = Column(
        String(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    token = Column(String(length=255), nullable=False)
    username = Column(String(length=255), nullable=False)
    expires_at = Column(DateTime, nullable=False)

