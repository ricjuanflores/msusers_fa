from typing import Optional, List
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from ms_fa.models import User, Profile
from ms_fa.repositories.repository import Repository
from ms_fa.repositories.user_repository import UserRepository
from ms_fa.repositories.role_repository import RoleRepository
from ms_fa.helpers.files import generate_client_filename, upload_file


class ShopperRepository(Repository[User]):
    def __init__(self, db: Session, cache=None):
        super().__init__(db)
        self.cache = cache
        self.userRepo = UserRepository(db, cache)
        self.roleRepo = RoleRepository(db)

    def get_model(self) -> type:
        return User

    def get_shopper_role(self):
        return self.roleRepo.find_by_attr("name", self._model._default_role)

    def add(self, data: dict) -> User:
        role = self.get_shopper_role()
        data["role_id"] = role.id
        user = self.userRepo.add(data)
        user.profile = Profile(data)
        self.db_save(user.profile)
        return user

    def update(self, id, data: dict) -> User:
        user = id if isinstance(id, User) else self.userRepo.find(id)
        if user.profile:
            user.profile.update(data)
            self.db_save(user)
        else:
            user.profile = Profile(data)
            self.db_save(user.profile)
        return user

    def upload_files(self, id, data: dict) -> User:
        user = id if isinstance(id, User) else self.userRepo.find(id)
        fields = ("legal_id_front", "legal_id_back", "proof_of_address")
        fields_url = {}
        
        for field in fields:
            if field not in data or data.get(field) is None:
                continue
            file = data.get(field)
            filename = generate_client_filename(user, file.filename)
            path = f"/tmp/{filename}"
            ext = path.split(".")[-1]
            destination = f"/shoppers/{user.id}/{field}.{ext}"
            
            # Save file to temp location
            with open(path, "wb") as buffer:
                buffer.write(file.file.read())
            
            url = upload_file(path, destination)
            fields_url[field] = url
        
        if len(fields_url) > 0:
            self.update(user, fields_url)
        return user

    def update_second_credit(self, id, second_credit: bool) -> User:
        user = self.userRepo.find(id)
        if user.profile:
            user.profile.second_credit = second_credit
            self.db_save(user)
        else:
            user.profile = Profile()
            user.profile.second_credit = second_credit
            self.db_save(user.profile)
        self.userRepo.setCache(user)
        return user

    def update_payment(self, id, data: dict) -> User:
        user = self.userRepo.find(id)
        if user.profile:
            user.profile.available_credit = data.get("available_credit", 0)
            user.profile.payment_capacity = data.get("payment_capacity", 0)
            self.db_save(user)
        else:
            user.profile = Profile()
            user.profile.available_credit = data.get("available_credit", 0)
            user.profile.payment_capacity = data.get("payment_capacity", 0)
            self.db_save(user.profile)
        self.userRepo.setCache(user)
        return user

    def update_available_credit(self, id, data: dict) -> User:
        user = self.userRepo.find(id)
        if user.profile:
            user.profile.available_credit = data.get("available_credit", 0)
            self.db_save(user)
        else:
            user.profile = Profile()
            user.profile.available_credit = data.get("available_credit", 0)
            self.db_save(user.profile)
        self.userRepo.setCache(user)
        return user

    def update_payment_capacity(self, id, data: dict) -> User:
        user = self.userRepo.find(id)
        if user.profile:
            user.profile.payment_capacity = data.get("payment_capacity", 0)
            self.db_save(user)
        else:
            user.profile = Profile()
            user.profile.payment_capacity = data.get("payment_capacity", 0)
            self.db_save(user.profile)
        self.userRepo.setCache(user)
        return user

    def update_kyc_prescoring(self, id, kyc_prescoring_id: int) -> User:
        user = self.userRepo.find(id)
        if user.profile:
            user.profile.kyc_prescoring_id = kyc_prescoring_id
            self.db_save(user)
        else:
            user.profile = Profile({"kyc_prescoring_id": kyc_prescoring_id})
            self.db_save(user.profile)
        return user

    def update_pay_id(self, id, pay_id: str) -> User:
        user = self.userRepo.find(id)
        if user.profile:
            user.profile.pay_id = pay_id
            self.db_save(user)
        else:
            user.profile = Profile({"pay_id": pay_id})
            self.db_save(user.profile)
        return user

    def create_profile_to_user(self, user, data: dict) -> User:
        user = self.userRepo.find(user)
        user.profile = Profile(data)
        self.db_save(user.profile)
        self.userRepo.setCache(user)
        return user

    def find_all_optional(
        self,
        filters: List,
        filtersSearch: List,
        fail: bool = True,
        paginate: bool = False,
        page: int = 1,
        per_page: int = 15
    ):
        q = self.db.query(self._model).join(Profile).filter(
            and_(*filters, or_(*filtersSearch))
        ).order_by(User.created_at.desc())
        
        if paginate:
            return self._paginate(q, page, per_page)
        return q.all()

