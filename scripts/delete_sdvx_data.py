#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path('.').resolve()))

from app import db
from app.api.games.sdvx.models import Music, Apeca

if __name__ == '__main__':
    for x in db.session.query(Music):
        db.session.delete(x)
    for x in db.session.query(Apeca):
        db.session.delete(x)
    db.session.commit()
