import dash
from dash import Dash, html

app = Dash(
    "ts_app",
    suppress_callback_exceptions=True,
    external_scripts=["https://cdn.plot.ly/plotly-2.22.0.min.js"],
    title="Time Series App",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
    use_pages=True,
)

app.layout = html.Div(dash.page_container)
