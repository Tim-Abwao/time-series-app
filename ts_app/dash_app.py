from dash import Dash

app = Dash(
    "ts_app",
    suppress_callback_exceptions=True,
    external_scripts=["https://cdn.plot.ly/plotly-basic-2.9.0.min.js"],
    title="Time Series App",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)
