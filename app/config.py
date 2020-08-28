import os

def _get(env_name, fallback=None):
    return os.environ.get(env_name, fallback)

class Config:
    APP_NAME = _get('APP_NAME', 'fairyjoke')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = _get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(BASE_DIR, '../app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = _get('SECRET_KEY', 'set a freaking key')
    LOGS_PATH = _get('LOGS_DIR', 'logs')
    ITEMS_LIMIT = 50
    MOMENT_DEFAULT_FORMAT='LLL'
    SDVX_PATH = None
    PUBLIC_URI = 'https://fairyjoke.net'
