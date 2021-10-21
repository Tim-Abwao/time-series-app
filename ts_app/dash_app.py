from dash import Dash

app = Dash(
    "ts_app",
    suppress_callback_exceptions=True,
    title="Time Series App",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)
