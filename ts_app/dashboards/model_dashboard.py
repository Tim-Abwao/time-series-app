import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import time
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.ts_functions import fit_arima_model
from ts_app.dashboards.dashboard_resources import ts_details


SOURCE = 'upload'
SAMPLE_PARAMS = html.Span()


def compile_layout(source=SOURCE, sample_params=SAMPLE_PARAMS):
    return html.Div([
        # Main title
        html.H1('Time Series Modelling'),

        # Container for the dashboard - a 2 column grid
        html.Div(className='dashboard', children=[
            # Side-bar with the parameter-selection menus
            html.Div(className='side-bar', children=[
                sample_params,
                # Model parameter selectors
                html.Div(id='model-params', children=[
                    html.H3('Model parameters'),
                    # AR order dropdown
                    html.P('AR Order'),
                    dcc.Dropdown(
                        id='model-ar', clearable=False, placeholder='AR order',
                        searchable=False, value=1,
                        options=[{'label': f'{i}', 'value': i}
                                 for i in range(1, 5)]),
                    # Differencing order dropdown
                    html.P('Differencing Order'),
                    dcc.Dropdown(
                        id='model-diff', clearable=False, value=1,
                        placeholder='Differencing', searchable=False,
                        options=[{'label': f'{i}', 'value': i}
                                 for i in range(1, 5)]),
                    # MA order dropdown
                    html.P('MA Order'),
                    dcc.Dropdown(
                        id='model-ma', clearable=False, placeholder='MA order',
                        searchable=False, value=1,
                        options=[{'label': f'{i}', 'value': i}
                                 for i in range(1, 5)])

                ])
            ]),  # End of the side-bar

            # Graph container
            html.Div(className='graph', children=[
                html.Div(dcc.Graph(id=f'{source}-graph')),
                html.Div(id='details', children=[
                    dcc.Markdown(ts_details)
                ])
            ])
        ])  # End of graph area

    ])  # End of app layout definition


layout = compile_layout(SOURCE, SAMPLE_PARAMS)


@app.callback(
    Output(f'{SOURCE}-graph', 'figure'),
    [Input('model-ar', 'value'),
     Input('model-diff', 'value'),
     Input('model-ma', 'value')]
)
def refit_arima_model(ar_order, diff_order, ma_order):
    """Fit an ARIMA model each time a model parameter is modified.

    Parameter:
    ---------
    ar_order, ma_order, diff_order: int
        The AR order, Differencing order & MA order for the ARIMA model."""
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

    sample_info = f'{sample.name}'

    fig.update_layout(
        paper_bgcolor='#eee', plot_bgcolor='#eee',
        title=f"An {model_info} model fitted on {sample_info}.")
    return fig
