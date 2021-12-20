#!/usr/bin/env python3

from pathlib import Path
import sys
import yaml
from yaml import Loader

sys.path.append(str(Path('.').resolve()))

from app import db
from app.models import Series, Game

path = Path('./data/games.yml')
data = yaml.load(path.read_text(), Loader)
print(data)

for series_short, series_info in data.items():
    series = db.create(
        Series,
        short=series_short,
        create_keys={'name': series_info['name']}
    )
    for game_short, game_name in series_info['games'].items():
        game = db.create(
            Game,
            short=game_short,
            create_keys={'name': game_name, 'series_short': series_short},
        )
