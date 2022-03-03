from pkgutil import get_data

from dash import dcc, html

page_content = get_data("ts_app", "assets/home-page.md").decode("utf-8")

layout = html.Div(
    className="home-page-content",
    children=[
        # Introduction
        dcc.Markdown(page_content),
        html.Div(
            className="footer",
            children=[
                html.A(
                    "Upload a file", href="/upload", className="button"
                ),
                html.A(
                    "Process a sample",
                    href="/sample",
                    className="button",
                ),
            ],
        ),
    ],
)
