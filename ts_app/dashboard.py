from dash import dcc, html
from dash.dependencies import Input, Output

from ts_app.dash_app import app
from ts_app.dashboard_components import (
    glossary,
    home_page,
    modelling,
    sample,
    upload,
)

server = app.server

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page(pathname: str) -> html.Div:
    """Display the page at the given pathname.

    Parameters
    ----------
    path_name : str
        The url to a page.

    Returns
    -------
    dash.html.Div.Div
        Page content.
    """
    if pathname == "/glossary":
        return glossary.layout
    elif pathname == "/sample":
        return generate_dashboard(data_source=sample.input_layout)
    elif pathname == "/upload":
        return generate_dashboard(data_source=upload.input_layout)
    else:
        return home_page.layout


def generate_dashboard(data_source: html.Div) -> html.Div:
    """Get a dashboard layout with the given `data_source`.

    Parameters
    ----------
    data_source : dash.html.Div.Div
        A html form to collect input

    Returns
    -------
    dash.html.Div.Div
        Dashboard layout.
    """
    return html.Div(
        id="dashboard-content",
        className="dashboard-content",
        children=[
            # Sidebar with input forms
            html.Div(
                className="side-bar",
                children=[
                    html.Div(data_source, id="data-source"),
                    dcc.Store(id="sample-data-store"),
                    dcc.Store(id="file-upload-store"),
                    modelling.model_param_input,
                ],
            ),
            # Time series forecasting plots and guide
            modelling.graphs_and_guide,
        ],
    )
