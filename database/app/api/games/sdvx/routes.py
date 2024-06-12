from datetime import date
from typing import List

from app import Schema, config, db
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse

from . import DATA_PATH, router
from .models import Apeca, Difficulties, Music


class DifficultySchema(Schema):
    diff: Difficulties
    level: int
    illustrator: str
    effector: str


class MusicSchema(Schema):
    title: str
    artist: str
    ascii: str
    bpm: str
    release_date: date
    version: int
    # genres: List[Genres]
    difficulties: List[DifficultySchema]


@router.get("/musics")
async def sdvx_get_musics():
    return {
        x.id: MusicSchema.model_validate(x) for x in db.session.query(Music)
    }


@router.get("/musics/{music_id}")
async def sdvx_get_music(music_id: int):
    music = db.session.get(Music, music_id)
    if not music:
        raise HTTPException(404)
    return MusicSchema.model_validate(music)


@router.get("/musics/{music_id}/{difficulty}.png")
async def sdvx_get_jacket(
    req: Request,
    music_id: int,
    difficulty: Difficulties,
    fallback=False,
    size=None,
):
    music = db.session.get(Music, music_id)
    if not music:
        raise HTTPException(404)
    diff = next(filter(lambda x: x.diff == difficulty, music.difficulties))
    if diff.external_jacket:
        return RedirectResponse(diff.external_jacket)
    folder = DATA_PATH / "music" / diff.music.folder

    if size and size == "big":
        filename = diff.jacket_big
    else:
        filename = diff.filename
    path = folder / filename

    if not path.exists():
        if fallback == "default":
            return RedirectResponse(req.url_for("sdvx_default_jacket"))
        if fallback == "game":
            return RedirectResponse(req.url_for("sdvx_default_version_jacket"))

        raise HTTPException(404)

    return FileResponse(path)


@router.get("/assets/jacket/version.png")
async def sdvx_default_version_jacket():
    path = DATA_PATH / "graphics" / "jk_dummy.png"
    if not path.exists():
        raise HTTPException(404)
    return FileResponse(path)


@router.get("/assets/jacket/no_data.png")
async def sdvx_default_jacket():
    path = config.DATA_PATH / "no_data.png"
    if not path.exists():
        raise HTTPException(404)
    return FileResponse(path)


@router.get("/apecas/{apeca_id}.png")
async def sdvx_get_apeca(apeca_id: int):
    apeca = db.session.get(Apeca, apeca_id)
    if not apeca:
        raise HTTPException(404)
    path = DATA_PATH / "graphics" / "ap_card" / f"{apeca.texture}.png"
    return FileResponse(path)
