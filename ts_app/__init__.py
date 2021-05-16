import logging
import webbrowser

from waitress import serve

from ts_app.dashboard import server

# Only log errors. `ConvergenceWarning`s and `ValueWarning`s are all too
# frequent when fitting the statsmodels ARIMA model on arbitrary data.
logging.basicConfig(level=logging.ERROR)
logging.captureWarnings(True)


__version__ = '0.1.1'


def run_app():
    """Start the app server, and launch a browser to view it."""

    # Open a new window of the default browser and point it to the where the
    # app is running.
    webbrowser.open('http://localhost:8000', new=1)

    # Serve the app using waitress
    print('Starting server at http://localhost:8000 ...')
    serve(server, host='localhost', port=8000)
