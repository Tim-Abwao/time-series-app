import dash

app = dash.Dash(__name__, url_base_pathname='/dashboard/',
                suppress_callback_exceptions=True)
server = app.server
