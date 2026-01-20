from ms_fa.tasks.worker import celery
from ms_fa.db import SessionLocal
from ms_fa.db.cache import Cache
from ms_fa.config import settings
from ms_fa.repositories import UserRepository, AppRepository, SessionRepository


@celery.task
def update_cache_task():
    """Task to update user and app cache from active sessions."""
    db = SessionLocal()
    cache = Cache(settings.redis_config)
    
    try:
        user_repo = UserRepository(db, cache)
        app_repo = AppRepository(db, cache)
        session_repo = SessionRepository(db)

        prefix = "ms-users-"
        users = session_repo.get_users_with_active_session()
        apps = app_repo.all()

        for u in users:
            if not cache.exists(f"{prefix}{u.id}"):
                user_repo.setCache(u, force=True)
        
        for a in apps:
            if not cache.exists(f"{prefix}{a.id}"):
                app_repo.setCache(a)
    finally:
        db.close()

