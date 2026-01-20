import uuid
from typing import List
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ms_fa.models.base import Model
from ms_fa.models.association_tables import app_permission_table, app_role_table


class App(Model):
    __tablename__ = 'app'

    _fillable = ['name', 'description']

    id = Column(
        String(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    name = Column(
        String(length=255),
        nullable=False,
        unique=True
    )
    description = Column(
        String(length=255),
        nullable=True
    )
    token = Column(
        String(length=1024),
        nullable=True
    )

    permissions = relationship(
        "Permission",
        lazy="dynamic",
        secondary=app_permission_table,
        passive_deletes=True
    )
    roles = relationship(
        "Role",
        lazy="dynamic",
        secondary=app_role_table,
        passive_deletes=True
    )

    @property
    def roles_permissions(self) -> List:
        permissions = list()
        roles = self.roles.all()
        for role in roles:
            permissions = list(set(permissions + role.permissions.all()))
        return permissions

    @property
    def all_permissions(self) -> List:
        permissions = self.permissions.all() or list()
        for p in self.roles_permissions:
            if p not in permissions:
                permissions.append(p)
        return permissions

    @property
    def roles_list(self) -> List[str]:
        roles = self.roles.all()
        roles_list = list()
        for role in roles:
            roles_list.append(role.name)
        return roles_list

