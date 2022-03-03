from pkgutil import get_data
from typing import Tuple

import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from statsmodels.tsa.api import seasonal_decompose
from ts_app import plotting
from ts_app.dash_app import app
from ts_app.ts_functions import create_arma_sample, fit_arima_model

summary = get_data("ts_app", "assets/summary.md").decode()

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

graphs_and_guide = html.Div(
    className="graphs-and-guide",
    children=[
        dcc.Loading(
            color="#777",
            children=[
                dcc.Graph(id="component-plots"),
            ],
        ),
        html.Div(
            className="line-plot-and-summary",
            children=[
                dcc.Loading(
                    color="#777",
                    children=[
                        dcc.Graph(
                            id="line-plot",
                            config={"toImageButtonOptions": {"format": "svg"}},
                        ),
                    ],
                ),
                dcc.Markdown(summary, className="guide"),
                html.Div(
                    className="footer",
                    children=[
                        html.A(
                            "Back to home",
                            href="/",
                            className="button",
                        ),
                        html.A(
                            "Browse glossary",
                            href="/glossary",
                            className="button",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    [
        Output("line-plot", "figure"),
        Output("component-plots", "figure"),
    ],
    [
        Input("model-ar", "value"),
        Input("model-diff", "value"),
        Input("model-ma", "value"),
        Input("url", "pathname"),
        Input("sample-data-store", "data"),
        Input("file-upload-store", "data"),
    ],
)
def model_and_predict(
    ar_order: int,
    diff_order: int,
    ma_order: int,
    input_source: str,
    sample: dict,
    upload: dict,
) -> Tuple[go.Figure, go.Figure]:
    """Fit an ARIMA model each time model parameters or input data are
    modified, then plot the results.

    Parameters
    ----------
    ar_order, ma_order, diff_order : int
        The AR order, Differencing order and MA order for the ARIMA model.
    input_souce : {"/upload", "/sample"}
        The data source.
    sample, upload : dict
        Stored sample-data or uploaded-file-data respectively.

    Returns
    -------
    tuple
        A line-plot of the forecast results, and subplots with seasonal
        decomposition estimates.
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
