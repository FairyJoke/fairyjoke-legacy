from typing import List
from fastapi import Request, Query
from fastapi.responses import RedirectResponse

from app import Router, db
from app.api.games.ddr.models import Music, Playstyles, Difficulty
from .. import templates


router = Router(__name__)


@router.get('/')
async def ddr_index():
    return RedirectResponse(router.url_path_for('ddr_musics'))


@router.get('/musics')
async def ddr_musics(
    req: Request, page: int = 1, *,
    text: str = Query(''),
    level: List[int] = Query([]),
    style: List[Playstyles] = Query([Playstyles.SP]),
    artist: str = Query(''),
):
    print(style)
    query = db.session.query(Difficulty).join(Music)
    if text:
        text = text.strip()
        query = query.filter(
            Music.title.ilike(f'%{text}%')
            | Music.title_yomigana.ilike(f'%{text}%')
            | Music.artist.ilike(f'%{text}%')
            | Music.label.ilike(f'%{text}%')
        )
    if level:
        query = query.filter(
            Difficulty.level.in_(level)
            & Difficulty.playstyle.in_(style)
        )
    if artist:
        query = query.filter(Music.artist == artist)
    query = db.session.query(Music).filter(Music.id.in_(x.music_id for x in query))
    query = query.order_by(Music.id)
    pager = db.paginate(query, page)
    return templates.render(
        'ddr_musics.html', req, pager=pager, styles=Playstyles,
        search=dict(level=level, style=style, text=text),
    )


@router.get('/musics/{music_id}')
async def ddr_music(req: Request, music_id: int):
    music = db.session.get(Music, music_id)
    return templates.render('ddr_music.html', req, music=music)
