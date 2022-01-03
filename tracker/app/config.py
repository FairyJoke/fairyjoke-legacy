import os


DB_URI = os.environ.get('DB_URI', 'sqlite:///app.db')
DB_API = os.environ.get('DB_API', 'http://localhost:57302')
