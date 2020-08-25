#!/bin/bash

python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/flask db upgrade
./.venv/bin/flask run
