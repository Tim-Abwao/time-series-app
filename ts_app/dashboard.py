import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.dashboard_components import (
    home_page, glossary, sample, upload, modelling, resources
)


app.index_string = resources.template

server = app.server


def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])


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
        data_source = upload.input_layout
    elif path_name == '/sample':
        data_source = sample.input_layout
    elif path_name == '/glossary':
        return glossary.layout
    else:
        return home_page.layout

    return html.Div(id='dashboard', className='dashboard', children=[
        html.Div(className='sidebar', children=[
            html.Div(data_source, id='data-source'),
            modelling.param_imput
        ]),
        html.Div([
            modelling.graph,

            html.Footer([
                html.A('Back to home', href='/', className='hvr-bob button'),
                html.A('Browse glossary', href='/glossary',
                       className='hvr-bob button')
            ])
        ])

    ])


if __name__ == '__main__':
    app.run_server(debug=True)
