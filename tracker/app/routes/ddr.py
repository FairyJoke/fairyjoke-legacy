from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel as Schema
import requests

from app import Router, config, db
from app.models.ddr import DDRScore


router = Router(__name__)


@router.get('/scores/{diff_id}')
async def get_ddr_scores(diff_id: int):
    response = requests.get(f'{config.DB_API}/api/games/ddr/diff/{diff_id}')
    # db_url = f'{config.DB_API}/ddr/musics/{music_id}'
    data = response.json()
    scores = db.session.query(DDRScore).filter_by(api_chart_id=diff_id)
    return scores.all()



class ScorePostSchema(Schema):
    class JudgesSchema(Schema):
        marvelous: int = 0
        perfect: int = 0
        great: int = 0
        good: int = 0
        miss: int = 0
        ok: int = 0

    title: str
    playstyle: Literal['Single', 'Double']
    difficulty: Literal['BEGINNER', 'BASIC', 'HARD', 'EXPERT', 'CHALLENGE']
    score: Optional[int]
    ex: Optional[int]
    max_combo: Optional[int]
    judges: Optional[JudgesSchema]
    clear: Optional[Literal['fail', 'play', 'clear', 'fc', 'gfc', 'pfc', 'mfc']]
    time: Optional[datetime]



@router.post('/scores/')
async def post_ddr_score(item: ScorePostSchema):
    title = item.title
    response = requests.get(f'{config.DB_API}/api/games/ddr/musics?title={title}')
    data = response.json()[0]
    for diff in data['difficulties']:
        if diff['name'] == item.difficulty and diff['playstyle'] == item.playstyle:
            chart_id = diff['id']
            break
    else:
        raise Exception('Chart not found')
    return db.add(
        DDRScore,
        api_chart_id=chart_id,
        score=item.score,
        ex_score=item.ex,
        judges=item.judges.dict() if item.judges else None,
        time=item.time,
        clear_type=item.clear,
        max_combo=item.max_combo,
    )
