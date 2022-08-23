from pkgutil import get_data

import dash
from dash import dcc, html

dash.register_page(__name__, path="/", chapati=777)

HOMEPAGE_TEXT = get_data("ts_app", "assets/home-page.md").decode("utf-8")
layout = html.Div(
    className="home-page-content",
    children=[
        # Introduction
        dcc.Markdown(HOMEPAGE_TEXT),
        html.Div(
            className="footer",
            children=[
                html.A("Upload a file", href="/upload", className="button"),
                html.A(
                    "Process a sample",
                    href="/sample",
                    className="button",
                ),
            ],
        ),
    ],
)
