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

# Use a custom HTML template
app.index_string = resources.template

server = app.server


app.layout = html.Div(
    # Display current page
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page(pathname):
    """Display the page at the given pathname.

    Parameters
    ----------
    path_name : str
        The url to a page or dashboard layout.
    """
    if pathname == "/upload":
        # Get the dashboard layout with input from uploaded files
        data_source = upload.input_layout
    elif pathname == "/sample":
        # Get the dashboard layout which generates sample input data
        data_source = sample.input_layout
    elif pathname == "/glossary":
        # Display the glossary page
        return glossary.layout
    else:
        # Display the home page
        return home_page.layout

    # If the pathname is "/upload" or "/sample", create the appropriate
    # dashboard.
    return html.Div(
        id="dashboard",
        className="dashboard",
        children=[
            # Sidebar with data & model input
            html.Div(
                className="sidebar",
                children=[
                    # `data_source`: dropdowns to create a sample, or a file
                    # upload button.
                    html.Div(data_source, id="data-source"),
                    # Container for sample data
                    dcc.Store(id="sample-data-store"),
                    # Container for uploaded data
                    dcc.Store(id="upload-data-store"),
                    # Dropdowns for setting model parameters
                    modelling.param_input,
                ],
            ),
            html.Div(
                [
                    # A line graph of the fitted model, with predictions and
                    # forecast.
                    modelling.graph,
                    # Paragraphs with time series information
                    dcc.Markdown(resources.ts_details),
                    # Footer links to "home" and "glossary"
                    html.Footer(
                        [
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
                        ]
                    ),
                ]
            ),
        ],
    )


if __name__ == "__main__":
    app.run_server(debug=True)
