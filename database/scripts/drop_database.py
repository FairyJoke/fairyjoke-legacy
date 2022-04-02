#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path('.').resolve()))

from app import db

if __name__ == '__main__':
    db.session.execute(f'DROP DATABASE IF EXISTS {sys.argv[1]};')
