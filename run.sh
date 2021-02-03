#!/usr/bin/env bash
# Activate virtual environment if present
if [ -d venv ]
    then source venv/bin/activate
fi

waitress-serve --listen=127.0.0.1:8000 ts_app:server
