from fastapi.responses import FileResponse

from app import db
from . import DATA_JACKETS, router
from .models import Music


@router.get('/musics/{music_id}.jpg')
async def ddr_get_jacket(music_id: int):
    music = await ddr_get_music(music_id)
    path = DATA_JACKETS / f'{music.label}_tn.jpg'
    return FileResponse(path)


@router.get('/musics/{music_id}')
async def ddr_get_music(music_id: int):
    music = db.session.get(Music, music_id)
    return music
