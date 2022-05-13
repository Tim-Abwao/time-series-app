import logging
import webbrowser

from waitress import serve

from ts_app.cli import process_cli_args
from ts_app.dashboard import server

__version__ = "0.8.0"

logging.basicConfig(level="INFO")

# Suppress benign queue warnings
logging.getLogger("waitress.queue").setLevel("ERROR")


def run_app(
    host: str = "0.0.0.0", port: int = 8000, launch_browser: bool = True
) -> None:
    """Start the app server, and launch a web browser to it.

    Args:
        host (str, optional): A host-name/IP address. Defaults to "0.0.0.0".
        port (int, optional): TCP port to listen at. Defaults to 8000.
        launch_browser (bool, optional): Whether to launch a web browser to
            view the app. Defaults to True.
    """
    if launch_browser is True:
        webbrowser.open(f"{host}:{port}")

    serve(server, host=host, port=port)


def _run_in_cli() -> None:
    """Start the app server using input collected from the command line
    interface.
    """
    args = process_cli_args()

    if not args.no_browser:
        webbrowser.open(f"{args.host}:{args.port}")

    serve(server, host=args.host.split("://")[-1], port=args.port)
