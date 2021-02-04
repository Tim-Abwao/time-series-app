import dash_core_components as dcc
import dash_html_components as html
from io import StringIO, BytesIO
import pandas as pd
import plotly.graph_objs as go
import os
import time
from base64 import b64decode
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.ts_functions import fit_arima_model, create_arma_sample
from ts_app.dashboards.dashboard_resources import ts_details
from ts_app.file_upload import process_upload


SOURCE = 'upload'
SAMPLE_PARAMS = html.Div([
    dcc.Upload(html.Button('Upload a file', className='hvr-bob button'),
               id='upload-data', min_size=10, accept='.csv,.xls,.xlsx'),
    html.P(id='file-info')])


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
        ]),  # End of graph area
        html.Footer([
            html.A('Back to home', href='/', className='hvr-bob button'),
            html.A('Browse glossary', href='/glossary',
                   className='hvr-bob button')
        ])
    ])  # End of app layout definition


layout = compile_layout(SOURCE, SAMPLE_PARAMS)


@app.callback(
    Output('file-info', 'children'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')]
)
def upload_file(contents, filename):
    """Validate and store uploaded files.

    parameters:
    ----------
    contents: str
        base64 encoded string with the file's contents
    filename: str
    """
    if contents:  # if a file is uploaded
        content_type, content_string = contents.split(',')
        decoded = b64decode(content_string)
        try:
            if 'csv' in filename:
                # If the user uploaded a CSV file
                df = pd.read_csv(StringIO(decoded.decode('utf-8')),
                                 index_col=0)
            elif 'xls' in filename:
                # If the user uploaded an excel file
                df = pd.read_excel(BytesIO(decoded), index_col=0)

            # Process the parsed data and return info if an error is present
            if (error := process_upload(df, filename)):
                return error

            return f'Analysing {filename}'

        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
    else:
        return ''  # No information since there's no file content


@app.callback(
    Output(f'{SOURCE}-graph', 'figure'),
    [Input('model-ar', 'value'),
     Input('model-diff', 'value'),
     Input('model-ma', 'value'),
     Input('file-info', 'children')]
)
def refit_arima_model(ar_order, diff_order, ma_order, info):
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
