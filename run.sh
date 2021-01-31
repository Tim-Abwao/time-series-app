#!/usr/bin/env bash
# Activate virtual environment if present
if [ -d venv ]
    then source venv/bin/activate
fi

gunicorn ts_app:server
