from typing import Optional
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ts_app.dash_app import app
from ts_app.dashboard_components import (
    glossary,
    home_page,
    modelling,
    resources,
    sample,
    upload,
)

app.index_string = resources.html_template
server = app.server

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page(pathname: str) -> Optional[html.Div]:
    """Display the page at the given pathname.

    Parameters
    ----------
    path_name : str
        The url to a page or dashboard layout.

    Returns
    -------
    Optional[dash_html_components.Div.Div]
        Dashboard content.
    """
    if pathname == "/glossary":
        return glossary.layout
    elif pathname == "/sample":
        data_input_form = sample.input_layout
    elif pathname == "/upload":
        data_input_form = upload.input_layout
    else:
        return home_page.layout

    # If pathname in {"/upload", "/sample"}, create the appropriate dashboard.
    return html.Div(
        id="dashboard",
        className="dashboard",
        children=[
            # Sidebar with data & model input forms
            html.Div(
                className="side-bar",
                children=[
                    html.Div(data_input_form, id="data-source"),
                    # Container for sample data
                    dcc.Store(id="sample-data-store"),
                    # Container for uploaded data
                    dcc.Store(id="upload-data-store"),
                    # Dropdowns for setting model parameters
                    modelling.param_input,
                ],
            ),
            # Time series plots
            html.Div(
                className="plots-and-text",
                children=[
                    html.Div(
                        className="line-plot",
                        children=[
                            modelling.lineplot,
                            dcc.Markdown(resources.ts_details),
                        ],
                    ),
                    html.Div(
                        modelling.component_plots, className="component-plot"
                    ),
                    html.Div(
                        className="footer",
                        children=[
                            html.A(
                                "Back to home",
                                href="/",
                                className="hvr-bob button",
                            ),
                            html.A(
                                "Browse glossary",
                                href="/glossary",
                                className="hvr-bob button",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    app.run_server(debug=True)
