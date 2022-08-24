import json
from pkgutil import get_data

import dash
from dash import html

dash.register_page(__name__)

GLOSSARY_DATA = json.loads(get_data("ts_app", "assets/glossary.json"))

title_definition_pairs = sum(  # Concatenate list comprehension items
    [
        [  # Each item is list with a single Div
            html.Div(
                id=item["title"].replace(" ", "-"),
                children=[
                    html.Dt(item["title"]),
                    html.Dd(item["definition"]),
                ],
            )
            for item in sorted(GLOSSARY_DATA, key=lambda x: x["title"])
        ]
    ],
    start=[],
)

layout = html.Div(
    [
        html.Div(
            className="glossary-content",
            children=[
                html.H2("Glossary of Time Series Terms"),
                html.Dl(title_definition_pairs),
            ],
        ),
        html.Div(
            className="footer",
            children=[html.A("Back to home", href="/", className="button")],
        ),
    ]
)
