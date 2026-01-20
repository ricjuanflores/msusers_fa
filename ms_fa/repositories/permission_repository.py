from typing import Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ms_fa.models import Permission
from ms_fa.repositories.repository import Repository


class PermissionRepository(Repository[Permission]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_model(self) -> type:
        return Permission

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

    def delete(self, id: str, fail: bool = True) -> Tuple[Optional[Permission], bool]:
        permission = self.find(id, fail=fail)
        if permission is not None:
            if permission.fixed:
                return permission, False
            self.db_delete(permission)
            return permission, True
        return permission, False

