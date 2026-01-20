from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ms_fa.models import Device
from ms_fa.repositories.repository import Repository


class DeviceRepository(Repository[Device]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_model(self) -> type:
        return Device

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
                    self._model.device_id.like(f"%{search}%"),
                    self._model.mark.like(f"%{search}%"),
                    self._model.model.like(f"%{search}%"),
                )
            )
        
        q = q.order_by(order_by())
        
        if paginate:
            return self._paginate(q, page, per_page)
        return q.all()

