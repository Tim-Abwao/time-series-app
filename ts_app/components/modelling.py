from typing import Optional, Tuple

import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, callback, dcc, html
from statsmodels.tsa.api import seasonal_decompose
from ts_app import plotting
from ts_app.ts_functions import create_arma_sample, fit_arima_model

model_param_input = html.Div(
    id="model-params",
    className="param-input",
    children=[
        html.H3("Model parameters"),
        # AR order dropdown
        html.Label("AR Order", htmlFor="model-ar"),
        dcc.Dropdown(
            id="model-ar",
            clearable=False,
            placeholder="AR order",
            searchable=False,
            value=1,
            options=[{"label": f"{i}", "value": i} for i in range(6)],
        ),
        # Differencing order dropdown
        html.Label("Differencing Order", htmlFor="model-diff"),
        dcc.Dropdown(
            id="model-diff",
            clearable=False,
            value=0,
            placeholder="Differencing",
            searchable=False,
            options=[{"label": f"{i}", "value": i} for i in range(6)],
        ),
        # MA order dropdown
        html.Label("MA Order", htmlFor="model-ma"),
        dcc.Dropdown(
            id="model-ma",
            clearable=False,
            placeholder="MA order",
            searchable=False,
            value=1,
            options=[{"label": f"{i}", "value": i} for i in range(6)],
        ),
    ],
)

seasonal_decomposition_plot = dcc.Loading(
    dcc.Graph(id="component-plots"), color="#777"
)

forecast_line_plot = dcc.Loading(
    dcc.Graph(
        id="line-plot", config={"toImageButtonOptions": {"format": "svg"}}
    ),
    color="#777",
)

EXPLANATORY_TEXT = """
### Guide

Graphs reveal the [trend](/glossary#Trend) in the data, and help assess the
**goodness of fit**. In general, a good model should reasonably replicate the
behaviour of the historical data.

Graphs also help discover [seasonal](/glossary#Seasonality) and
[cyclic patterns](/glossary#Cyclic-patterns). These usually manifest as
occasional peaks or troughs.

[Autocorrelation][1] and [Partial-Autocorrelation][2] plots can provide hints
on a potentially suitable model to start with. [This article][3] describes how.
Testing for [stationarity][4], and filtering out seasonal & trend effects is
an essential first step.

[1]: https://en.wikipedia.org/wiki/Autocorrelation
[2]: https://en.wikipedia.org/wiki/Partial_autocorrelation_function
[3]: https://en.wikipedia.org/wiki/Box%E2%80%93Jenkins_method#Autocorrelation_\
and_partial_autocorrelation_plots
[4]: https://cran.r-project.org/web/packages/TSTutorial/vignettes/Stationary\
.pdf

"""

footer_buttons = html.Div(
    [
        html.A("Back to home", href="/", className="button"),
        html.A("Browse glossary", href="/glossary", className="button"),
    ],
    className="footer",
)


def generate_layout(input_source: html.Div) -> html.Div:
    """Get a dashboard layout with the given `input_source`.

    Args:
        input_source (dash.html.Div.Div): A html form to collect input.

    Returns:
        dash.html.Div.Div: Dashboard layout.
    """
    return html.Div(
        id="dashboard-content",
        className="dashboard-content",
        children=[
            # Current path
            dcc.Location(id="current-page"),
            # Sidebar with input forms
            html.Div(
                className="side-bar",
                children=[
                    html.Div(input_source, id="data-source"),
                    dcc.Store(id="sample-data-store"),
                    dcc.Store(id="file-upload-store"),
                    model_param_input,
                ],
            ),
            # Time series forecasting plots and guide
            html.Div(
                className="graphs-and-guide",
                children=[
                    seasonal_decomposition_plot,
                    html.Div(
                        [
                            forecast_line_plot,
                            dcc.Markdown(EXPLANATORY_TEXT, className="guide"),
                            footer_buttons,
                        ],
                        className="line-plot-and-summary",
                    ),
                ],
            ),
        ],
    )


@callback(
    [
        Output("line-plot", "figure"),
        Output("component-plots", "figure"),
    ],
    [
        Input("model-ar", "value"),
        Input("model-diff", "value"),
        Input("model-ma", "value"),
        Input("current-page", "pathname"),
        Input("sample-data-store", "data"),
        Input("file-upload-store", "data"),
    ],
)
def model_and_predict(
    ar_order: int,
    diff_order: int,
    ma_order: int,
    input_source: str,
    sample: Optional[dict],
    upload: Optional[dict],
) -> Tuple[go.Figure, go.Figure]:
    """Fit an ARIMA model each time model parameters or input data are
    modified, then plot the results.

    Args:
        ar_order (int): AR order.
        diff_order (int): Differencing order.
        ma_order (int): MA order.
        input_source (str): The data source.
        sample (Optional[dict]): Stored sample data, if any.
        upload (Optional[dict]): Uploaded data, if any.

    Returns:
        Tuple[Figure, Figure]: A line-plot of the forecast results, and
        subplots with seasonal decomposition estimates.
    """

    if input_source == "/upload" and upload is not None:
        filename = upload["filename"]
        data = pd.read_json(upload["data"], orient="index", typ="series")
    elif input_source == "/sample" and sample is not None:
        filename = sample["filename"]
        data = pd.read_json(sample["data"], orient="index", typ="series")
    else:
        filename = "a random sample"
        data = create_arma_sample()

    predictions, forecast = fit_arima_model(
        data, ar_order, diff_order, ma_order
    )

    line_plot = plotting.plot_forecast(
        actual_data=data,
        predictions=predictions,
        forecast=forecast,
        model_info=f"ARIMA({ar_order}, {diff_order}, {ma_order})",
        file_name=filename,
    )

    components = seasonal_decompose(data)
    component_subplots = plotting.plot_ts_components(
        trend=components.trend,
        seasonal=components.seasonal,
        residuals=components.resid,
        file_name=filename,
    )

    return line_plot, component_subplots
