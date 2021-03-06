import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ts_app.dash_app import app
from ts_app.dashboards import sample_dashboard, upload_dashboard


# Fetch page template
with open('ts_app/templates/dash_template.html') as template:
    app.index_string = template.read()

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard/upload':
        return upload_dashboard.layout
    else:
        return sample_dashboard.layout


if __name__ == '__main__':
    app.run_server(debug=True)
