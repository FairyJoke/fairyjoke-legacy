#!/bin/bash

python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/flask db upgrade
if [ "$1" == 'prod' ]; then
	FLASK_RUN_PORT=57310 ./.venv/bin/flask run
else
	FLASK_DEBUG=1 FLASK_RUN_PORT=57310 ./.venv/bin/flask run
fi
