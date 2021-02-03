from ts_app.flask_app import server
import os
from waitress import serve
import webbrowser


def run_app():
    """Start the app server, and launch a browser to view it."""

    # Open a tab in default browser and point it to the app
    webbrowser.open('http://localhost:8000')

    # Serve the app using waitress
    serve(server, host='localhost', port=8000)

    # Remove the temporary data store
    if os.path.isfile('ts-app-data.temp'):
        os.remove('ts-app-data.temp')
