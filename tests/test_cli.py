import sys

from ts_app.cli import process_cli_args


def test_default_args(monkeypatch):
    """Check whether default arguments are set."""
    monkeypatch.setattr(sys, "argv", ["ts_app"])
    args = process_cli_args()

    assert args.host == "localhost"
    assert args.port == 8000
    assert args.no_browser is False


def test_supplied_args(monkeypatch):
    """Check whether input arguments are collected."""
    monkeypatch.setattr(
        sys,
        "argv",
        "ts_app -p 25000 --host https://example.com --no-browser".split(),
    )
    args = process_cli_args()

    assert args.host == "https://example.com"
    assert args.port == 25000
    assert args.no_browser is True
