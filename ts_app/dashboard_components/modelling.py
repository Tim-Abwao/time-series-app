import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os
import time
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.ts_functions import fit_arima_model, create_arma_sample


param_imput = html.Div(id='model-params', children=[
    html.H3('Model parameters'),
    # AR order dropdown
    html.P('AR Order'),
    dcc.Dropdown(
        id='model-ar', clearable=False, placeholder='AR order',
        searchable=False, value=1,
        options=[{'label': f'{i}', 'value': i} for i in range(1, 5)]),
    # Differencing order dropdown
    html.P('Differencing Order'),
    dcc.Dropdown(
        id='model-diff', clearable=False, value=1,
        placeholder='Differencing', searchable=False,
        options=[{'label': f'{i}', 'value': i} for i in range(1, 5)]),
    # MA order dropdown
    html.P('MA Order'),
    dcc.Dropdown(
        id='model-ma', clearable=False, placeholder='MA order',
        searchable=False, value=1,
        options=[{'label': f'{i}', 'value': i} for i in range(1, 5)])
])

graph = html.Div(className='graph-container', children=[
    dcc.Loading([
        dcc.Graph(id='time-series-graph')
    ])
])


@app.callback(
    Output('time-series-graph', 'figure'),
    [Input('model-ar', 'value'),
     Input('model-diff', 'value'),
     Input('model-ma', 'value')]
)
def refit_arima_model(ar_order, diff_order, ma_order):
    """Fit an ARIMA model each time a model parameter is modified.

    Parameters:
    ---------
    ar_order, ma_order, diff_order: int
        The AR order, Differencing order & MA order for the ARIMA model.
    info: str
        Output from the upload-processing function. Included here to trigger
        model re-fitting on file upload.
    """
    time.sleep(1)
    if os.path.isfile('ts-app-data.temp'):
        data = pd.read_pickle('ts-app-data.temp')
    else:
        data = create_arma_sample()
    predictions, forecast = fit_arima_model(
        data, ar_order, diff_order, ma_order
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data,
                             mode='lines', name='actual data'))
    fig.add_trace(go.Scatter(x=predictions.index, y=predictions,
                             mode='lines',  name='predictions'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast,
                             mode='lines', name='forecast'))

    model_info = f"ARIMA({ar_order}, {diff_order}, {ma_order})"

    sample_info = f'{data.name}'

    fig.update_layout(
        paper_bgcolor='#eee', plot_bgcolor='#eee',
        title=f"An {model_info} model fitted on {sample_info}")
    return fig
