from ts_app.cli import process_cli_args


def test_default_args():
    """Check whether default arguments are set."""
    args = process_cli_args()

    assert args.host == "localhost"
    assert args.port == 8000
    assert args.no_browser is False


def test_supplied_args():
    """Check whether input arguments are collected."""
    args = process_cli_args(
        "-p", "25000", "--host", "example.com", "--no-browser"
    )

    assert args.host == "example.com"
    assert args.port == 25000
    assert args.no_browser is True
