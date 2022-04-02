import os
from pathlib import Path


DB_URI = os.environ.get('DB_URI', 'sqlite:///app.db')

DATA_PATH = Path('./data')
