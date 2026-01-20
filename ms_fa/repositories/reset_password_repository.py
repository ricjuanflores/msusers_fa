from typing import Optional
from sqlalchemy.orm import Session

from ms_fa.models import ResetPassword
from ms_fa.repositories.repository import Repository


class ResetPasswordRepository(Repository[ResetPassword]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_model(self) -> type:
        return ResetPassword

    def get_by_token(self, token: str, fail: bool = True) -> Optional[ResetPassword]:
        return self.find_by_attr("token", token, fail=fail)

    def get_by_token_and_username(self, token: str, username: str, fail: bool = True) -> Optional[ResetPassword]:
        q = self.db.query(self._model).filter_by(token=token, username=username)
        result = q.first()
        if fail and result is None:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Token not found")
        return result

