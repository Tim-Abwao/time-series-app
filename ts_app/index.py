import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.dashboards.dashboard_resources import template
from ts_app.dashboards import (
    home_page, glossary, sample_dashboard, upload_dashboard
)


app.index_string = template

server = app.server


def serve_layout():
    return html.Div([dcc.Location(id='url', refresh=False),
                     html.Div(id='page-content')])


app.layout = serve_layout


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(path_name):
    """Render the appropriate dashboard layout for the given path_name.

    Parameters:
    ----------
    path_name: str
    """
    if path_name == '/upload':
        return upload_dashboard.layout
    elif path_name == '/sample':
        return sample_dashboard.layout
    elif path_name == '/glossary':
        return glossary.layout
    else:
        return home_page.layout


if __name__ == '__main__':
    app.run_server(debug=True)
