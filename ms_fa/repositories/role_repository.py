from typing import Optional, Tuple, List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ms_fa.models import Role
from ms_fa.repositories.repository import Repository


class RoleRepository(Repository[Role]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_model(self) -> type:
        return Role

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

    def update(self, id: str, data: dict, fail: bool = True) -> Tuple[Optional[Role], bool]:
        role = self.find(id, fail=fail)
        if role is not None:
            if role.name == "root":
                return role, False
            role.update(data)
            self.db_save(role)
        return role, True

    def sync_permissions(self, id: str, permissions: List[str]):
        from ms_fa.repositories import PermissionRepository
        
        permissionRepo = PermissionRepository(self.db)
        role = self.find(id)
        role.permissions = list()
        for permission_id in permissions:
            permission = permissionRepo.find(permission_id)
            role.permissions.append(permission)
        self.db_save(role)

    def delete(self, id: str, fail: bool = True) -> Tuple[Optional[Role], bool]:
        role = self.find(id, fail=fail)
        if role is not None:
            if role.fixed:
                return role, False
            self.db_delete(role)
            return role, True
        return role, False

