from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def a():
    from apps
