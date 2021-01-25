#!/usr/bin/env bash
# Activate virtual environment if present
if [ -d venv ]
    then source venv/bin/activate
fi

export FLASK_APP=ts_app
export FLASK_ENV=development
echo $(which python)
flask run
