from base64 import b64decode
from io import BytesIO, StringIO
from typing import Optional, Tuple

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
                        html.Li("At least 32 rows"),
                    ]
                ),
            ],
            min_size=32,
            max_size=1024 ** 2 * 7,  # 7MiB
        ),
        # Container for the file-name or error message
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
def upload_file(
    contents: str, filename: str
) -> Tuple[str, dict, Optional[dict]]:
    """Extract, validate and process data from uploaded files.

    parameters
    ----------
    contents : str
        Base64-encoded string with the file's contents
    filename : str
        The name of the uploaded file

    Returns
    -------
    Tuple[str, dict, dict]
        (file-info message, file-info style, data to store).
    """
    if contents is None:
        return (
            "",  # No file information
            {},  # No special style
            None,  # No data to store
        )
    else:
        content_string = contents.split(",")[1]

    file_content = b64decode(content_string)

    try:
        if ".csv" in filename:
            df = pd.read_csv(
                StringIO(file_content.decode("utf-8")), index_col=0
            )
        elif ".xls" in filename:
            df = pd.read_excel(BytesIO(file_content), index_col=0)
    except Exception as e:
        print(e)
        return (
            html.Div(["There was an error processing the file."]),
            {"color": "orangered"},
            None,  # No data to store
        )

    if (error := process_upload(data=df)) is not None:
        return (
            error,
            {"color": "orangered"},
            None,  # No data to store
        )
    else:
        # If file-upload and data-extraction succeed
        return (
            f"Analysing {filename}",
            {"color": "#31bf2c"},
            {"filename": filename, "data": df.iloc[:, -1].to_json()},
        )
