import json
from pkgutil import get_data

import dash_html_components as html

# Get glossary data from the ts_app package as bytes
glossary_data = get_data("ts_app", "assets/glossary.json")

# Get the glossary data as a json object
definitions = json.loads(glossary_data.decode())


components = sum(  # Concatenate the list of title-definition pairs
    [
        [
            html.Dt(item["title"], id=item["title"]),
            html.Dd(item["definition"], id=item["definition"]),
        ]
        for item in definitions
    ],
    start=[],
)

layout = html.Div(
    [
        html.H2("Glossary of Time Series Terms"),
        html.Dl(components),  # Descriptions list
        html.Footer(
            [html.A("Back to home", href="/", className="hvr-bob button")]
        ),
    ]
)
