#!/bin/bash

venv=${VENV:-.venv}
[ -d "$venv" ] || python -m venv "$venv"
source "$venv/bin/activate"
pip install --upgrade -r requirements.txt
alembic upgrade head
uvicorn app:app --reload --host 127.0.0.1 --port "${1:-57302}"
