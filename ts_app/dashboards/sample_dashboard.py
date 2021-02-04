import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import time
from ts_app.dash_app import app
from ts_app.dashboards.upload_dashboard import compile_layout
from ts_app.ts_functions import fit_arima_model, create_arma_sample


SOURCE = 'sample'
SAMPLE_PARAMS = html.Div(id='sample-params', children=[
                html.H3('Sample parameters'),
                # AR order dropdown
                html.P('AR Order'),
                dcc.Dropdown(
                    id='sample-ar', clearable=False, placeholder='AR order',
                    searchable=False, value=1,
                    options=[{'label': f'{i}', 'value': i}
                             for i in range(1, 5)]),
                # MA order dropdown
                html.P('MA Order'),
                dcc.Dropdown(
                    id='sample-ma', clearable=False, placeholder='MA order',
                    searchable=False, value=1,
                    options=[{'label': f'{i}', 'value': i}
                             for i in range(1, 5)])
            ])


layout = compile_layout(SOURCE, SAMPLE_PARAMS)


@app.callback(
    Output('details', 'title'),
    [Input('sample-ar', 'value'),
     Input('sample-ma', 'value')]
)
def get_sample(ar_order, ma_order):
    """Create an ARMA sample with the given parameters.

    Parameters:
    ----------
    ar_order, ma_order: int
        AR order and MA order respectively.
    """
    sample = create_arma_sample(ar_order, ma_order, size=200)

    # Persist sample
    sample.rename('sample').to_pickle('ts-app-data.temp')
    return 'details'


@app.callback(
    Output(f'{SOURCE}-graph', 'figure'),
    [Input('model-ar', 'value'),
     Input('model-diff', 'value'),
     Input('model-ma', 'value'),
     Input('sample-ar', 'value'),
     Input('sample-ma', 'value')]
)
def refit_arima_model(ar_order, diff_order, ma_order, sample_ar, sample_ma):
    """Fit an ARIMA model each time a model parameter is modified.

    Parameter:
    ---------
    ar_order, diff_order, ma_order, sample_ar, sample_ma: int
        The AR order, Differencing order & MA order for the ARIMA model; and
        the AR order and MA order for the sample."""
    time.sleep(1)
    sample = pd.read_pickle('ts-app-data.temp')
    predictions, forecast = fit_arima_model(
        sample, ar_order, diff_order, ma_order
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sample.index, y=sample,
                             mode='lines', name='actual data'))
    fig.add_trace(go.Scatter(x=predictions.index, y=predictions,
                             mode='lines',  name='predictions'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast,
                             mode='lines', name='forecast'))

    model_info = f"ARIMA({ar_order}, {diff_order}, {ma_order})"

    sample_info = f'an ARMA({sample_ar}, {sample_ma}) sample'

    fig.update_layout(
        paper_bgcolor='#eee', plot_bgcolor='#eee',
        title=f"An {model_info} model fitted on {sample_info}")
    return fig
