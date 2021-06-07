import argparse


def process_cli_args(*args):
    """Create arguments and collect input from the command line."""
    parser = argparse.ArgumentParser(
        prog="ts_app",
        description="A simple dashboard application to learn time series"
        + " basics and interactively fit ARIMA models.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The TCP port on which to listen (default: %(default)s).",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="A host-name or IP address (default: %(default)r).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Avoid openning a browser tab or window.",
    )
    if args:  # Parse supplied args. Helpful in tests.
        print(args)
        return parser.parse_args(args)
    else:  # Parse arguments from `sys.argv`
        return parser.parse_args()
