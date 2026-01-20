import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model


class Session(Model):
    __tablename__ = 'session'

    _fillable = [
        "user_id",
        "token",
        "expires_at",
    ]

    id = Column(
        String(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    user_id = Column(
        String(length=36),
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    token = Column(String(250), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")

