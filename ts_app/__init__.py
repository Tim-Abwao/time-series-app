import logging
import sys
import threading
import webbrowser

import waitress

from ts_app.cli import process_cli_args
from ts_app.dash_app import app

__version__ = "0.9.1"

logging.basicConfig(level="INFO")

# Suppress benign queue warnings
logging.getLogger("waitress.queue").setLevel("ERROR")


def custom_hook(type, value, traceback) -> None:
    """Custom exception handler to allow clean stopping of the app server
    using `CTRL + C` i.e. KeyboardInterrupt.

    Args:
        type (Exception): The unhandled exception encountered.
        value (str): The exception's arg(s).
        traceback (traceback): Stack trace object.
    """
    if type is KeyboardInterrupt:
        print("\nServer Stopped.")
        exit()
    else:
        print(type, value)


sys.excepthook = custom_hook


def run_app(
    host: str = "localhost", port: int = 8000, launch_browser: bool = True
) -> None:
    """Start the app server, and launch a web browser to it.

    Args:
        host (str, optional): A host-name/IP address. Defaults to "localhost".
        port (int, optional): TCP port to listen at. Defaults to 8000.
        launch_browser (bool, optional): Whether to launch a web browser to
            view the app. Defaults to True.
    """
    server_ = threading.Thread(
        target=waitress.serve,
        kwargs=dict(app=app.server, host=host, port=port),
    )
    server_.start()

    if launch_browser is True:
        webbrowser.open(f"{host}:{port}")

    server_.join()


def _run_in_cli() -> None:
    """Start the app server using input collected from the command line
    interface.
    """
    args = process_cli_args()

    run_app(
        host=args.host.split("://")[-1],
        port=args.port,
        launch_browser=not args.no_browser,  # True if `no_browser` is not set
    )
