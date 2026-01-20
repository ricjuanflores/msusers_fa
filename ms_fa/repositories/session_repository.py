import datetime
from typing import Optional, List
from sqlalchemy.orm import Session as DBSession

from ms_fa.models import Session, User
from ms_fa.repositories.repository import Repository


class SessionRepository(Repository[Session]):
    def __init__(self, db: DBSession):
        super().__init__(db)

    def get_model(self) -> type:
        return Session

    def delete(self, user, token: str) -> Optional[Session]:
        user_id = user.id if isinstance(user, User) else user
        session = self.db.query(self._model).filter_by(
            user_id=user_id,
            token=token
        ).first()
        if session:
            self.db_delete(session)
        return session

    def has_active_session(self, user) -> bool:
        user_id = user.id if isinstance(user, User) else user
        now = datetime.datetime.utcnow()
        count = self.db.query(self._model).filter(
            self._model.user_id == user_id,
            self._model.expires_at > now
        ).count()
        return count > 0

    def get_users_with_active_session(self) -> List[User]:
        now = datetime.datetime.utcnow()
        sessions = self.db.query(self._model).filter(
            self._model.expires_at > now
        ).all()
        users = []
        for session in sessions:
            if session.user not in users:
                users.append(session.user)
        return users

