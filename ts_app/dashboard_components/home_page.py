import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    className="home-page-content",
    children=[
        # Introduction
        dcc.Markdown(
            """
# Time Series App

---

A simple application that illustrates basic [time series analysis][1]
techniques. A [glossary](/glossary) of terms is available to help get familiar
with the main concepts.

In a nutshell, Time Series Analysis purposes to learn and emulate the
behaviour of data over time. Time Series Forecasting then leverages this
insight to estimate future values.

![An example of time series analysis results, plotted](/assets/ts.svg)

To give it a try, you can upload a file or create a sample to analyse:

[1]: https://en.wikipedia.org/wiki/Time_series
"""
        ),
        html.Div(
            className="footer",
            children=[
                html.A(
                    "Upload a file", href="/upload", className="hvr-bob button"
                ),
                html.A(
                    "Process a sample",
                    href="/sample",
                    className="hvr-bob button",
                ),
            ],
        ),
    ],
)
