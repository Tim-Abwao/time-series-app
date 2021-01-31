import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from ts_app.ts_functions import fit_arima_model
import plotly.graph_objs as go
import pandas as pd
import time
from ts_app.dash_app import app


with open('ts_app/dashboards/details.md') as file:
    details = file.read()

layout = html.Div([
    # Main title
    html.H1('Time Series Modelling'),

    # Container for the dashboard - a 2 column grid
    html.Div(className='dashboard', children=[
        # Side-bar with the parameter-selection menus
        html.Div(className='side-bar', children=[
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
            html.Div(dcc.Graph(id='upload-graph')),
            html.Div(id='details', children=[
                dcc.Markdown(details)
            ])
        ])
    ])  # End of graph area

])  # End of app layout definition


@app.callback(
    Output('upload-graph', 'figure'),
    [Input('model-ar', 'value'),
     Input('model-ma', 'value'),
     Input('model-diff', 'value')]
)
def refit_arima_model(ar_order, ma_order, diff_order):
    """Fit an ARIMA model each time a model parameter is modified.

    Parameter:
    ---------
    ar_order, ma_order, diff_order: int
        The AR order, MA order, Differencing order for the ARIMA model."""
    time.sleep(1)
    sample = pd.read_pickle('sample.pkl')
    predictions, forecast = fit_arima_model(
        sample, ar_order, ma_order, diff_order
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
