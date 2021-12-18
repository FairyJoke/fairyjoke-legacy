from fastapi import Request

from app import Router, db
from app.api.games import sdvx
from .. import templates


router = Router(__name__)

@router.get('/')
async def index(req: Request, page: int = 1):
    query = db.session.query(sdvx.models.Music)
    musics = db.paginate(query, page)
    return templates.render('sdvx.html', req, pager=musics)
