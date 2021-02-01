#!/usr/bin/env bash
# Activate virtual environment if present
if [ -d venv ]
    then source venv/bin/activate
fi

gunicorn -w 3 ts_app:server
