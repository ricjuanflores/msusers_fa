import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model
from ms_fa.models.association_tables import permission_role_table


class Role(Model):
    __tablename__ = 'role'

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

    permissions = relationship(
        "Permission",
        lazy='dynamic',
        secondary=permission_role_table,
        passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<role id={self.id} name={self.name}>"

