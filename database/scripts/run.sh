#!/bin/bash

venv=${VENV:-.venv}
[ -d "$venv" ] || python -m venv "$venv"
source "$venv/bin/activate"
pip install --upgrade -r requirements.txt
alembic upgrade head
uvicorn app:app --reload --host 0.0.0.0 --port "${1:-57302}"
