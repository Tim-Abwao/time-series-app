import logging
import os
import webbrowser

from waitress import serve

from ts_app.dashboard import server

# Only log errors. `ConvergenceWarning`s and `ValueWarning`s are all too
# frequent when fitting the statsmodels ARIMA model on arbitrary data.
logging.basicConfig(level=logging.ERROR)
logging.captureWarnings(True)


__version__ = '0.1.0'


def run_app():
    """Start the app server, and launch a browser to view it."""

    # Open a tab in default browser and point it to the app
    webbrowser.open('http://localhost:8000', new=1)

    # Serve the app using waitress
    print('Starting server at http://localhost:8000 ...')
    serve(server, host='localhost', port=8000)

    # Remove the temporary data store
    if os.path.isfile('ts-app-data.temp'):
        os.remove('ts-app-data.temp')
