from base64 import b64decode
from io import BytesIO, StringIO

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.file_upload import process_upload


input_layout = html.Div([
    # File upload button
    dcc.Upload(
        id='upload-data', accept='.csv,.xls,.xlsx', min_size=10,
        children=[
            html.Button('Upload a file', className='hvr-bob button'),
        ]),
    html.P(id='file-info')
])


@app.callback(
    [Output('file-info', 'children'),
     Output('file-info', 'style'),
     Output('upload-data-store', 'data')],
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')]
)
def upload_file(contents, filename):
    """Validate, process and store uploaded files.

    parameters
    ----------
    contents : str
        base64 encoded string with the file's contents
    filename : str
        The name of the uploaded file

    Returns
    -------
    A tuple, (file_info message, file_info style, target data store).
    """
    if contents is None:
        return '', {}, None
    else:
        content_type, content_string = contents.split(',')
    # Decode file content
    file_content = b64decode(content_string)

    try:
        if 'csv' in filename:
            # If the user uploaded a CSV file
            df = pd.read_csv(StringIO(file_content.decode('utf-8')),
                             index_col=0)
        elif 'xls' in filename:
            # If the user uploaded an excel file
            df = pd.read_excel(BytesIO(file_content), index_col=0)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the file.'
        ]), {'color': 'orangered'}, None
    # Process the parsed data and return info if an error is present
    if (error := process_upload(df, filename)) is not None:
        return error, {'color': 'orangered'}, None

    return (
        f'Analysing {filename}',
        {'color': '#31bf2c'},
        {
            'filename': filename,
            'data': df.iloc[:, -1].to_json()
        }
    )
