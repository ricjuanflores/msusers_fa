import datetime
from typing import Optional, List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ms_fa.models import User, Profile
from ms_fa.repositories.repository import Repository


class UserRepository(Repository[User]):
    def __init__(self, db: Session, cache=None):
        super().__init__(db)
        self.cache = cache
        self.rootRole = "root"
        self.cache_key_prefix = "ms-users-"

    def get_model(self) -> type:
        return User

    def add(self, data: dict) -> User:
        from ms_fa.repositories import RoleRepository
        
        roleRepo = RoleRepository(self.db)
        role_id = data.get("role_id") if "role_id" in data else roleRepo.find_by_attr("name", self._model._default_role).id
        role = roleRepo.find(role_id)
        
        user = self._model(data)
        user.roles.append(role)
        
        if "password" in data:
            user.new_pass = True
            user.set_password(data["password"])
        else:
            return None
        
        self.db_save(user)
        return user

    def all(
        self,
        search: str = None,
        order_column: str = "created_at",
        order: str = "desc",
        paginate: bool = False,
        page: int = 1,
        per_page: int = 15,
        deleted: bool = False
    ):
        column = getattr(self._model, order_column)
        order_by = getattr(column, order)
        q = self.db.query(self._model).outerjoin(Profile)
        
        if search is not None:
            q = q.filter(
                or_(
                    self._model.id.like(f"%{search}%"),
                    self._model.email.like(f"%{search}%"),
                    self._model.phone.like(f"%{search}%"),
                    self._model.name.like(f"%{search}%"),
                    self._model.lastname.like(f"%{search}%"),
                    Profile.curp.like(f"%{search}%"),
                    Profile.rfc.like(f"%{search}%"),
                )
            )
        
        if not deleted:
            q = q.filter(self._model.deleted_at.is_(None))
        else:
            q = q.filter(self._model.deleted_at.is_not(None))
        
        q = q.order_by(order_by())
        
        if paginate:
            return self._paginate(q, page, per_page)
        return q.all()

    def find(self, id: str, fail: bool = True, with_deleted: bool = False) -> Optional[User]:
        if isinstance(id, self._model):
            return id
        filters = {"id": id}
        if not with_deleted:
            filters["deleted_at"] = None
        q = self.db.query(self._model).filter_by(**filters)
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result

    def find_by_attr(self, column: str, value, fail: bool = True, with_deleted: bool = False) -> Optional[User]:
        q = self.db.query(self._model).filter_by(**{column: value})
        if not with_deleted:
            q = q.filter(self._model.deleted_at.is_(None))
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result

    def find_optional(self, filter: dict, fail: bool = True, with_deleted: bool = False) -> Optional[User]:
        filters = [getattr(self._model, key) == val for key, val in filter.items()]
        q = self.db.query(self._model).filter(or_(*filters))
        if not with_deleted:
            q = q.filter(self._model.deleted_at.is_(None))
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result

    def find_by_phone_and_email(self, phone: str, email: str, fail: bool = True, with_deleted: bool = False) -> Optional[User]:
        filters = {"phone": phone, "email": email}
        if not with_deleted:
            filters["deleted_at"] = None
        q = self.db.query(self._model).filter_by(**filters)
        result = q.first()
        if fail and result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result

    def update_password(self, id, password: str, fail: bool = True) -> User:
        user = self.find(id, fail)
        if user is not None:
            user.new_pass = True
            user.set_password(password)
            self.db_save(user)
        return user

    def update_available_credit(self, id, amount: float):
        user = id if isinstance(id, self._model) else self.find(id)
        user.profile.available_credit = amount
        self.db_save(user)

    def update_payment_capacity(self, id, amount: float):
        user = id if isinstance(id, self._model) else self.find(id)
        user.profile.payment_capacity = amount
        self.db_save(user)

    def update_second_credit(self, id, has_second_credit: bool):
        user = id if isinstance(id, self._model) else self.find(id)
        user.profile.second_credit = has_second_credit
        self.db_save(user)

    def sync_permissions(self, id: str, permissions: List[str]):
        from ms_fa.repositories import PermissionRepository
        
        permissionRepo = PermissionRepository(self.db)
        user = self.find(id)
        user.permissions = list()
        for permission_id in permissions:
            permission = permissionRepo.find(permission_id)
            user.permissions.append(permission)
        self.db_save(user)
        self.setCache(user)

    def sync_roles(self, id: str, roles: List[str]):
        from ms_fa.repositories import RoleRepository
        
        roleRepo = RoleRepository(self.db)
        user = self.find(id)
        user.roles = list()
        for role_id in roles:
            role = roleRepo.find(role_id)
            user.roles.append(role)
        self.db_save(user)
        self.setCache(user)

    def activate(self, id: str, fail: bool = True) -> User:
        user = self.find(id, fail=fail)
        if user is not None and not user.is_active:
            user.is_active = True
            self.db_save(user)
        return user

    def deactivate(self, id: str, fail: bool = True) -> User:
        user = self.find(id, fail=fail)
        if user is not None and user.is_active:
            user.is_active = False
            self.db_save(user)
        return user

    def soft_delete(self, id: str, fail: bool = True) -> User:
        user = self.find(id, fail=fail)
        if user is not None and user.deleted_at is None:
            self.canBeDeleted(user)
            user.deleted_at = datetime.datetime.now()
            self.db_save(user)
            self.deleteCache(user)
        return user

    def restore(self, id: str, fail: bool = True) -> User:
        user = self.find(id, fail=fail, with_deleted=True)
        if user is not None and user.deleted_at is not None:
            user.deleted_at = None
            self.db_save(user)
            self.setCache(user)
        return user

    def delete(self, id: str, fail: bool = True) -> User:
        user = self.find(id, fail=fail, with_deleted=True)
        if user is not None:
            self.canBeDeleted(user)
            user.permissions = list()
            user.roles = list()
            self.db_delete(user)
            self.deleteCache(user)
        return user

    def canBeDeleted(self, user: User):
        if self.rootRole in user.roles_list:
            raise HTTPException(status_code=403, detail="You can't delete root user")

    def setCache(self, user: User, force: bool = False):
        if self.cache is None:
            return
            
        key = f"{self.cache_key_prefix}{user.id}"

        if not self.cache.exists(key) and not force:
            return

        permissions = [p.name for p in user.all_permissions]
        data = {
            "id": user.id,
            "email": user.email,
            "permissions": permissions,
            "roles": user.roles_list,
            "profile": None,
        }

        if hasattr(user, "profile") and user.profile is not None:
            data["profile"] = {
                "payment_capacity": user.profile.payment_capacity,
                "second_credit": user.profile.second_credit,
                "available_credit": user.profile.available_credit,
            }

        self.cache.set(key, data)

    def deleteCache(self, user: User):
        if self.cache is None:
            return
        self.cache.delete(f"{self.cache_key_prefix}{user.id}")

