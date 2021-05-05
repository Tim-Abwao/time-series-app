import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.ts_functions import create_arma_sample, fit_arima_model


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
     Input('model-ma', 'value'),
     Input('url', 'pathname'),
     Input('sample-data-store', 'data'),
     Input('upload-data-store', 'data')]
)
def refit_arima_model(
        ar_order, diff_order, ma_order, input_source, sample, upload):
    """Fit an ARIMA model each time a model parameter is modified.

    Parameters
    ----------
    ar_order, ma_order, diff_order : int
        The AR order, Differencing order & MA order for the ARIMA model.
    input_souce : {'/upload', '/sample'}
        The data source.
    sample, upload : dash_core_components.Store
        Store objects containing the sample data and uploaded-file data
        respectively.
    """
    if input_source == '/upload':
        data_store = upload
    elif input_source == '/sample':
        data_store = sample

    if data_store is None:
        filename = 'sample'
        data = create_arma_sample()
    else:
        filename = data_store['filename']
        json_data = data_store['data']
        data = pd.read_json(json_data, orient='index', typ='series')

    predictions, forecast = fit_arima_model(
        data, ar_order, diff_order, ma_order
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data, x=data.index,
                             mode='lines', name='actual data'))
    fig.add_trace(go.Scatter(x=predictions.index, y=predictions,
                             mode='lines',  name='predictions'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast,
                             mode='lines', name='forecast'))

    model_info = f"ARIMA({ar_order}, {diff_order}, {ma_order})"

    fig.update_layout(
        paper_bgcolor='#eee', plot_bgcolor='#eee',
        title=f"An {model_info} model fitted on {filename}")
    return fig
