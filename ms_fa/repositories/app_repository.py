from typing import Optional, List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ms_fa.models import App
from ms_fa.repositories.repository import Repository


class AppRepository(Repository[App]):
    def __init__(self, db: Session, cache=None):
        super().__init__(db)
        self.cache = cache
        self.cache_key_prefix = "ms-users-"

    def get_model(self) -> type:
        return App

    def all(
        self,
        search: str = None,
        order_column: str = 'created_at',
        order: str = 'desc',
        paginate: bool = False,
        page: int = 1,
        per_page: int = 15
    ):
        column = getattr(self._model, order_column)
        order_by = getattr(column, order)
        q = self.db.query(self._model)
        
        if search is not None:
            q = q.filter(
                or_(
                    self._model.id.like(f"%{search}%"),
                    self._model.name.like(f"%{search}%"),
                )
            )
        
        q = q.order_by(order_by())
        
        if paginate:
            return self._paginate(q, page, per_page)
        return q.all()

    def update_token(self, app: App, token: str):
        app.token = token
        self.db_save(app)

    def sync_permissions(self, id: str, permissions: List[str]):
        from ms_fa.repositories import PermissionRepository
        
        permissionRepo = PermissionRepository(self.db)
        app = self.find(id)
        app.permissions = list()
        for permission_id in permissions:
            permission = permissionRepo.find(permission_id)
            app.permissions.append(permission)
        self.db_save(app)
        self.setCache(app)

    def sync_roles(self, id: str, roles: List[str]):
        from ms_fa.repositories import RoleRepository
        
        roleRepo = RoleRepository(self.db)
        app = self.find(id)
        app.roles = list()
        for role_id in roles:
            role = roleRepo.find(role_id)
            app.roles.append(role)
        self.db_save(app)
        self.setCache(app)

    def setCache(self, app: App):
        if self.cache is None:
            return
            
        key = f"{self.cache_key_prefix}{app.id}"
        permissions = [p.name for p in app.all_permissions]
        data = {
            "id": app.id,
            "permissions": permissions,
            "roles": app.roles_list,
        }
        self.cache.set(key, data)

