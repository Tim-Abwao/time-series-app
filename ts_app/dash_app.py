from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from ts_app.ts_sample import create_arma_sample
from ts_app.fit_time_series import fit_arima_model
import plotly.graph_objs as go
import pandas as pd
import time


app = Dash(__name__, url_base_pathname='/dashboard/')
server = app.server


with open('ts_app/templates/dash_template.html') as text:
    app.index_string = text.read()


app.layout = html.Div([
    html.H1('Time Series Modelling'),
    html.Div(className='dashboard', children=[
        html.Div(className='side-bar', children=[
            # Sample parameters
            html.Div(id='sample-params', children=[
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
            ]),
            # Model parameters
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
        ],

        ),

        html.Div(className='graph', children=[
            html.Div(dcc.Graph(id='ts-graph')),
            html.Div(id='details')
        ])
    ])
])


@app.callback(
    Output('details', 'children'),
    [Input('sample-ar', 'value'),
     Input('sample-ma', 'value')]
)
def get_sample(ar_order, ma_order):
    sample = create_arma_sample(ar_order, ma_order, size=100)

    # Persist sample
    sample.rename('sample').to_pickle('sample.pkl')

    details = """
Graphs help **visualise the trend** in the data. They clearly reveal whether
there's been an increase, decrease or no change in the data values over time.

Graphs also help **discover seasonal** and **cyclic patterns** present in the
data. These usually manifest as occasional peaks or troughs.

Testing for [stationarity][1], and filtering out seasonal & trend effects is an
essential first step. Model fitting usually requires that the time series data
be stationary, and may even contain transformations to make the data
stationary.

Graphs are also useful in **assessing the goodness of fit**. In general, a good
model should reasonably replicate the behaviour of the data used.

[Autocorrelation][2] and [Partial-Autocorrelation][3] plots can provide hints
on a potentially suitable model to start with. [This article][4] describes how.

[1]: https://cran.r-project.org/web/packages/TSTutorial/vignettes/\
Stationary.pdf
[2]: https://en.wikipedia.org/wiki/Autocorrelation
[3]: https://en.wikipedia.org/wiki/Partial_autocorrelation_function
[4]: https://en.wikipedia.org/wiki/Box%E2%80%93Jenkins_method#Autocorrelation\
_and_partial_autocorrelation_plots
"""
    return dcc.Markdown(details)


@app.callback(
    Output('ts-graph', 'figure'),
    [Input('model-ar', 'value'),
     Input('model-ma', 'value'),
     Input('model-diff', 'value'),
     Input('sample-ar', 'value'),
     Input('sample-ma', 'value')]
)
def refit_arima_model(ar_order, ma_order, diff_order, sample_ar, sample_ma):
    time.sleep(1)
    sample = pd.read_pickle('sample.pkl')
    predictions, forecast, _ = fit_arima_model(
        sample, ar_order, ma_order, diff_order)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sample.index, y=sample,
                             mode='lines', name='actual data'))
    fig.add_trace(go.Scatter(x=predictions.index, y=predictions,
                             mode='lines',  name='predictions'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast,
                             mode='lines', name='forecast'))

    model_info = f"ARIMA({ar_order}, {diff_order}, {ma_order})"

    if sample.name == 'sample':
        sample_info = f'an ARMA({sample_ar}, {sample_ma}) sample'
    else:
        sample_info = f'{sample.name}'

    fig.update_layout(
        paper_bgcolor='#eee', plot_bgcolor='#eee',
        title=f"An {model_info} model fitted on {sample_info}.")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
