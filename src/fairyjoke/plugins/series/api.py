from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_series():
    return {"series": []}
