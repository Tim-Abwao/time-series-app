#!/usr/bin/env bash
# Activate virtual environment if present
if [ -d venv ]
    then source venv/bin/activate
fi

waitress-serve --listen=103.70.29.102:8000 ts_app:server
