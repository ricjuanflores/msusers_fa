import uuid
from sqlalchemy import Column, String, Boolean
from ms_fa.models.base import Model


class Permission(Model):
    __tablename__ = 'permission'

    _fillable = ['name', 'fixed']

    id = Column(
        String(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    name = Column(
        String(length=120),
        unique=True,
        nullable=False
    )
    fixed = Column(
        Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return f"<permission id={self.id} name={self.name}>"

