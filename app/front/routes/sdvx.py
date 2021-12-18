from fastapi import Request

from app import Router, db
from app.api.games import sdvx
from .. import templates


router = Router(__name__)


@router.get('/songs')
async def list_songs(req: Request, page: int = 1):
    query = db.session.query(sdvx.models.Music)
    pager = db.paginate(query, page)
    return templates.render('sdvx_songs.html', req, pager=pager)


@router.get('/apecas')
async def list_apecas(req: Request, page: int = 1):
    query = db.session.query(sdvx.models.Apeca)
    pager = db.paginate(query, page, 60)
    return templates.render('sdvx_apecas.html', req, pager=pager)
