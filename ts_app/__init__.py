import logging
import webbrowser

from waitress import serve

from ts_app.dashboard import server

__version__ = "0.1.1"

# Set logging level to INFO
logging.basicConfig(level="INFO")

# Set waitress.queue logging level to ERROR
logging.getLogger("waitress.queue").setLevel("ERROR")


def run_app(host="localhost", port=8000):
    """Start the app server, and launch a browser to view it.

    Parameters
    ----------
    host : str, optional
        A host-name or IP address, default "localhost"
    port : int, optional
        The TCP port on which to listen, default 8000
    """

    # Open a new window of the default browser and point it to the where the
    # app is running.
    webbrowser.open(f"http://{host}:{port}", new=1)

    # Serve the app using waitress
    serve(server, host=host, port=port)
