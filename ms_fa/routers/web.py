from fastapi import APIRouter

web_router = APIRouter(tags=["Web"])


@web_router.get("/")
async def index():
    return {"message": "Welcome to MS Users FastAPI"}

