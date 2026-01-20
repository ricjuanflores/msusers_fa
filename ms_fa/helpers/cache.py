from fastapi import Request


def get_cache(request: Request):
    return request.app.state.cache


def update_cache():
    from ms_fa.db import SessionLocal
    from ms_fa.repositories import UserRepository, AppRepository, SessionRepository

    db = SessionLocal()
    try:
        userRepo = UserRepository(db)
        appRepo = AppRepository(db)
        sessionRepo = SessionRepository(db)

        prefix = "ms-users-"
        users = sessionRepo.get_users_with_active_session()
        apps = appRepo.all()

        # Note: This requires access to the cache, which in FastAPI
        # would typically be passed as a parameter
        # For now, this is a placeholder for the cache update logic
    finally:
        db.close()

