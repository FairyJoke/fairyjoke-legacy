import functools
from typing import List, Optional
from fastapi import Request, Query

from app import Router, Schema, db
from app.api.games.sdvx.models import Apeca, Difficulty, Music, GENRES
from .. import templates


router = Router(__name__)


class SearchSchema(Schema):
    level: Optional[List[int]]
    genre: Optional[List[int]]
    text: Optional[str]


@router.get('/musics')
async def sdvx_musics(
    req: Request, page: int = 1,  *,
    level: List[int] = Query([]),
    genre: List[int] = Query([]),
    text: str = Query(''),
):
    query = db.session.query(Difficulty).join(Music)
    if level:
        query = query.filter(Difficulty.level.in_(map(int, level)))
    if genre:
        genre_mask = functools.reduce(lambda a, b: a | b, genre)
        query = query.filter(
            (Music.genre.op('&')(genre_mask) == genre_mask)
            | (Music.genre == 0 if 0 in genre else Music.genre != None)
        )
    if text:
        query = query.filter(
            Music.title.ilike(f'%{text}%')
            | Music.artist.ilike(f'%{text}%')
            | Music.ascii.ilike(f'%{text}%')
            | Difficulty.illustrator.ilike(f'%{text}%')
            | Difficulty.effector.ilike(f'%{text}%')
        )
    query = db.session.query(Music).filter(Music.id.in_(x.music_id for x in query))
    pager = db.paginate(query, page)
    return templates.render(
        'sdvx_musics.html', req,
        pager=pager, genres=GENRES,
        search=dict(level=level, genre=genre, text=text),
    )


@router.get('/musics/{music_id}')
async def sdvx_music(music_id: int, req: Request,):
    music = db.session.get(Music, music_id)
    return templates.render('sdvx_music.html', req, music=music)


@router.get('/apecas')
async def sdvx_apecas(req: Request, page: int = 1):
    query = db.session.query(Apeca)
    pager = db.paginate(query, page, 60)
    return templates.render('sdvx_apecas.html', req, pager=pager)
