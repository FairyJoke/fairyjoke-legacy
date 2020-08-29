import click
from flask import current_app

from .consumer import import_from_game_data
from . import bp

@bp.cli.command()
@click.argument('path')
def load_data(path):
    import_from_game_data(path)

@bp.cli.command()
def init():
    return import_from_game_data(current_app.config.get('SDVX_PATH'), current_app.config.get('SDVX_EXTRA_PATH'))
