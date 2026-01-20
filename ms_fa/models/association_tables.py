from sqlalchemy import Table, Column, ForeignKey
from ms_fa.db import Base


permission_role_table = Table(
    "role_has_permissions",
    Base.metadata,
    Column('role_id', ForeignKey('role.id', ondelete='CASCADE')),
    Column('permission_id', ForeignKey('permission.id')),
)

user_permission_table = Table(
    "user_has_permissions",
    Base.metadata,
    Column('user_id', ForeignKey('user.id', ondelete='CASCADE')),
    Column('permission_id', ForeignKey('permission.id')),
)

user_role_table = Table(
    "user_has_roles",
    Base.metadata,
    Column('user_id', ForeignKey('user.id', ondelete='CASCADE')),
    Column('role_id', ForeignKey('role.id')),
)

app_permission_table = Table(
    "app_has_permissions",
    Base.metadata,
    Column('app_id', ForeignKey('app.id', ondelete='CASCADE')),
    Column('permission_id', ForeignKey('permission.id')),
)

app_role_table = Table(
    "app_has_roles",
    Base.metadata,
    Column('app_id', ForeignKey('app.id', ondelete='CASCADE')),
    Column('role_id', ForeignKey('role.id')),
)

