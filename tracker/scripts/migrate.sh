#!/bin/bash

./scripts/generate_models_init_file.py

[ -d .venv ] && source .venv/bin/activate

alembic upgrade head
alembic revision --autogenerate -m "$*"
