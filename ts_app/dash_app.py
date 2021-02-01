from dash import Dash

app = Dash(__name__, url_base_pathname='/dashboard/', title="Time Series App",
           suppress_callback_exceptions=True)
