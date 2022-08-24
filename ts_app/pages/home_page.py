import dash
from dash import dcc, html

dash.register_page(__name__, path="/", chapati=777)

HOMEPAGE_TEXT = """
# Time Series App

---

A simple application that illustrates basic [time series analysis][ts-wiki]
concepts. A [glossary](/glossary) of terms is available to help get started.

You can upload a file, or generate sample data, then interactively fit
[ARIMA][arima] models.

In a nutshell, *Time Series Analysis* purposes to learn and emulate the
behaviour of data over time. *Time Series Forecasting* then leverages this
insight to estimate future values.

![An example of time series analysis results, plotted](/assets/ts.svg)

[ts-wiki]: https://en.wikipedia.org/wiki/Time_series
[arima]: https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_\
average
"""

layout = html.Div(
    className="home-page-content",
    children=[
        # Introduction
        dcc.Markdown(HOMEPAGE_TEXT),
        html.Div(
            className="footer",
            children=[
                html.A("Upload a file", href="/upload", className="button"),
                html.A(
                    "Process a sample",
                    href="/sample",
                    className="button",
                ),
            ],
        ),
    ],
)
