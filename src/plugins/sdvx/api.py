from fastapi import APIRouter

router = APIRouter()


# TODO
@router.get("/songs")
async def get_songs():
    return {"songs": []}
