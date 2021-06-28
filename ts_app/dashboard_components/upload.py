from base64 import b64decode
from io import BytesIO, StringIO

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.file_upload import process_upload

input_layout = html.Div(
    [
        # File upload button
        dcc.Upload(
            id="upload-data",
            accept=".csv,.xls,.xlsx",
            className="file-upload",
            children=[
                "Click or Drag and Drop",
                html.P("Expected file properties:"),
                html.Ul(
                    children=[
                        html.Li("At most 7MiB"),
                        html.Li("Dates in first column"),
                        html.Li("Numeric data in right-most column"),
                    ]
                ),
            ],
            min_size=32,
            max_size=1024 ** 2 * 7,  # 7MiB
        ),
        # Container for the filename or error message
        html.P(id="file-info"),
    ]
)


@app.callback(
    [
        Output("file-info", "children"),
        Output("file-info", "style"),
        Output("upload-data-store", "data"),
    ],
    [Input("upload-data", "contents"), Input("upload-data", "filename")],
)
def upload_file(contents, filename):
    """Extract, validate and process data from uploaded files.

    parameters
    ----------
    contents : str
        Base64-encoded string with the file's contents
    filename : str
        The name of the uploaded file

    Returns
    -------
    A tuple - (file_info message, file_info style, data to store).
    """
    if contents is None:
        # If no file has been uploaded
        return (
            "",  # No file information
            {},  # No special style
            None,  # No data to store
        )
    else:
        content_type, content_string = contents.split(",")

    # Decode file content
    file_content = b64decode(content_string)

    # Pack the contents in a DataFrame
    try:
        if ".csv" in filename:
            # If the user uploaded a CSV file
            df = pd.read_csv(
                StringIO(file_content.decode("utf-8")), index_col=0
            )
        elif ".xls" in filename:
            # If the user uploaded an excel file
            df = pd.read_excel(BytesIO(file_content), index_col=0)
    except Exception as e:
        print(e)
        return (
            html.Div(["There was an error processing the file."]),
            {"color": "orangered"},  # Error-message text color
            None,  # No data to store
        )

    # Process the parsed data
    if (error := process_upload(data=df)) is not None:
        # If an error message is returned
        return (
            error,  # Error message
            {"color": "orangered"},  # Error-message text color
            None,  # No data to store
        )
    else:
        # If file-upload and data-extraction succeed
        return (
            f"Analysing {filename}",  # Uploaded file's name
            {"color": "#31bf2c"},  # Successful-upload text color
            {"filename": filename, "data": df.iloc[:, -1].to_json()},
        )
