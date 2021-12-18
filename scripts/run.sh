#!/bin/bash

[ -d .venv ] || python -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
uvicorn app:app --reload --port "${1:-57302}"
