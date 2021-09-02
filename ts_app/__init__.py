import logging
import webbrowser

from waitress import serve

from ts_app.cli import process_cli_args
from ts_app.dashboard import server

__version__ = "0.4.0"

logging.basicConfig(level="INFO")

# Suppress benign queue warnings
logging.getLogger("waitress.queue").setLevel("ERROR")


def run_app(
    host: str = "http://localhost",
    port: int = 8000,
    launch_browser: bool = True,
) -> None:
    """Start the app server, and launch a web browser to it.

    Parameters
    ----------
    host : str, optional
        A host-name or IP address, default "http://localhost"
    port : int, optional
        The TCP port on which to listen, default 8000
    launch_browser : bool
        Whether or not to launch a web browser to view the app
    """
    if launch_browser is True:
        webbrowser.open(f"{host}:{port}")

    serve(server, host=host.lstrip("http://"), port=port)


def run_in_cli() -> None:
    """Start the app server using input collected from the command line
    interface.
    """
    args = process_cli_args()

    if not args.no_browser:
        webbrowser.open(f"{args.host}:{args.port}")

    serve(server, host=args.host.lstrip("http://"), port=args.port)
