from typing import Tuple
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from statsmodels.tsa.api import seasonal_decompose
from ts_app.dash_app import app
from ts_app.ts_functions import create_arma_sample, fit_arima_model

param_input = html.Div(
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

lineplot = html.Div(
    className="lineplot",
    children=[
        dcc.Loading(
            color="#777",
            children=[
                dcc.Graph(id="time-series-graph"),
            ],
        )
    ],
)

component_plots = html.Div(
    className="subplots",
    children=[
        dcc.Loading(
            color="#777",
            children=[
                dcc.Graph(id="component-plots"),
            ],
        )
    ],
)


@app.callback(
    [
        Output("time-series-graph", "figure"),
        Output("component-plots", "figure"),
    ],
    [
        Input("model-ar", "value"),
        Input("model-diff", "value"),
        Input("model-ma", "value"),
        Input("url", "pathname"),
        Input("sample-data-store", "data"),
        Input("upload-data-store", "data"),
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
    if input_source == "/upload":
        data_store = upload
    elif input_source == "/sample":
        data_store = sample

    if data_store is None:  # Default if there's no data
        filename = "a random sample"
        data = create_arma_sample()
    else:
        filename = data_store["filename"]
        json_data = data_store["data"]
        data = pd.read_json(json_data, orient="index", typ="series")

    predictions, forecast = fit_arima_model(
        data, ar_order, diff_order, ma_order
    )

    lineplot = go.Figure()
    lineplot.add_trace(
        go.Scatter(y=data, x=data.index, mode="lines", name="actual data")
    )
    lineplot.add_trace(
        go.Scatter(
            x=predictions.index,
            y=predictions,
            mode="lines",
            name="predictions",
        )
    )
    lineplot.add_trace(
        go.Scatter(x=forecast.index, y=forecast, mode="lines", name="forecast")
    )
    model_info = f"ARIMA({ar_order}, {diff_order}, {ma_order})"
    lineplot.update_layout(
        paper_bgcolor="#eee",
        plot_bgcolor="#eee",
        height=350,
        title=f"An {model_info} model fitted on {filename}",
    )
    lineplot.update_xaxes(fixedrange=True)
    lineplot.update_yaxes(fixedrange=True)

    components = seasonal_decompose(data)
    residuals = components.resid
    seasonal = components.seasonal
    trend = components.trend
    components_subplots = make_subplots(
        rows=3,
        cols=1,
        subplot_titles=("Residuals", "Seasonal", "Trend"),
        shared_xaxes=True,
    )
    components_subplots.add_trace(
        go.Scatter(x=residuals.index, y=residuals, name="residuals"),
        row=1,
        col=1,
    )
    components_subplots.add_trace(
        go.Scatter(x=seasonal.index, y=seasonal, name="seasonal"), row=2, col=1
    )
    components_subplots.add_trace(
        go.Scatter(x=trend.index, y=trend, name="trend"), row=3, col=1
    )
    components_subplots.update_layout(
        height=540,
        paper_bgcolor="#eee",
        plot_bgcolor="#eee",
        showlegend=False,
        title="Seasonal Decomposition",
    )
    components_subplots.update_xaxes(fixedrange=True)
    components_subplots.update_yaxes(fixedrange=True)

    return lineplot, components_subplots
