#!/bin/bash

[ -d .venv ] && source .venv/bin/activate

alembic upgrade head
alembic revision --autogenerate -m "$*"
