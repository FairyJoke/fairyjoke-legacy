from fairyjoke import Plugin

router = Plugin.Router()


# TODO
@router.get("/songs")
async def get_songs():
    return {"songs": []}
