import datetime
import uuid
from typing import List, Optional
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256

from ms_fa.models.base import Model
from ms_fa.models.association_tables import user_permission_table, user_role_table


class User(Model):
    __tablename__ = "user"

    _default_role = "shopper"

    _fillable = [
        "phone",
        "email",
        "name",
        "lastname",
        "second_lastname",
    ]

    id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    name = Column(String(50), nullable=True)
    lastname = Column(String(50), nullable=True)
    second_lastname = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    aq_id = Column(Integer, nullable=True)
    new_pass = Column(Boolean, default=True, nullable=True)
    deleted_at = Column(DateTime, default=None, nullable=True)

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all,delete",
    )
    devices = relationship(
        "Device",
        back_populates="user",
        cascade="all,delete",
    )
    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all,delete",
    )
    permissions = relationship(
        "Permission",
        lazy="dynamic",
        secondary=user_permission_table,
        passive_deletes=True
    )
    roles = relationship(
        "Role",
        lazy="dynamic",
        secondary=user_role_table,
        passive_deletes=True
    )

    def __repr__(self):
        return f"<user id={self.id} email={self.email} phone={self.phone}>"

    @property
    def fullname(self) -> str:
        return f"{self.name} {self.lastname} {self.second_lastname}"

    def set_password(self, password: str) -> None:
        self.password = pbkdf2_sha256.using(rounds=100000, salt_size=12).hash(password)

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

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

