import json
from pkgutil import get_data

import dash_html_components as html

# Get glossary data as binary string
glossary_data = get_data("ts_app", "assets/glossary.json")

definitions = json.loads(glossary_data.decode())

title_definition_pairs = sum(  # Concatenate
    [
        [
            html.Dt(item["title"], id=item["title"]),
            html.Dd(item["definition"], id=item["definition"]),
        ]
        for item in sorted(definitions, key=lambda x: x["title"])
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
            children=[
                html.A("Back to home", href="/", className="hvr-bob button")
            ],
        ),
    ]
)
