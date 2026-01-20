from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar, Generic
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    def __init__(self, db: Session) -> None:
        self.db = db
        self._model = self.get_model()

    @abstractmethod
    def get_model(self) -> type:
        pass

    def db_save(self, model: Any = None) -> None:
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
        except Exception as e:
            self.rollback()
            raise e

    def db_bulk_save(self, models: List[Any]) -> None:
        try:
            self.db.bulk_save_objects(models)
            self.db.commit()
        except Exception as e:
            self.rollback()
            raise e

    def db_delete(self, model: Any) -> None:
        try:
            self.db.delete(model)
            self.db.commit()
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self) -> None:
        self.db.rollback()

    def add(self, data: dict) -> T:
        model = self._model(data)
        self.db_save(model)
        return model

    def all(
        self,
        order_column: str = 'created_at',
        order: str = 'desc',
        paginate: bool = False,
        page: int = 1,
        per_page: int = 15
    ):
        column = getattr(self._model, order_column)
        order_by = getattr(column, order)
        q = self.db.query(self._model).order_by(order_by())
        
        if paginate:
            return self._paginate(q, page, per_page)
        return q.all()

    def _paginate(self, query, page: int, per_page: int):
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        pages = (total + per_page - 1) // per_page
        
        return {
            'items': items,
            'page': page,
            'pages': pages,
            'per_page': per_page,
            'prev': page - 1 if page > 1 else None,
            'next': page + 1 if page < pages else None,
            'total': total,
        }

    def find(self, id: str, fail: bool = True) -> Optional[T]:
        if isinstance(id, self._model):
            return id
        q = self.db.query(self._model).filter_by(id=id)
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        return result

    def find_by_attr(self, column: str, value: Any, fail: bool = True) -> Optional[T]:
        q = self.db.query(self._model).filter_by(**{column: value})
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        return result

    def find_optional(self, filter: dict, fail: bool = True) -> Optional[T]:
        filters = [
            getattr(self._model, key) == val 
            for key, val in filter.items()
        ]
        q = self.db.query(self._model).filter(or_(*filters))
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        return result

    def find_all_optional(
        self,
        filter: dict,
        fail: bool = True,
        paginate: bool = False,
        page: int = 1,
        per_page: int = 15
    ):
        filters = [
            getattr(self._model, key) == val 
            for key, val in filter.items()
        ]
        q = self.db.query(self._model).filter(or_(*filters))
        
        if paginate:
            return self._paginate(q, page, per_page)
        return q.all()

    def update(self, id: str, data: dict, fail: bool = True) -> Optional[T]:
        model = self.find(id, fail=fail)
        if model is not None:
            model.update(data)
            self.db_save(model)
        return model

    def delete(self, id: str, fail: bool = True) -> Optional[T]:
        model = self.find(id, fail=fail)
        if model is not None:
            self.db_delete(model)
        return model

