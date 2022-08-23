from base64 import b64decode
from io import BytesIO, StringIO
from typing import Optional, Tuple

import dash
import pandas as pd
from dash import Input, Output, callback, dcc, html
from ts_app.components import modelling
from ts_app.file_upload import process_upload

dash.register_page(__name__)

file_upload_component = html.Div(
    [
        dcc.Upload(
            id="file-upload",
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
            max_size=1024**2 * 7,  # 7MiB
        ),
        html.P(id="file-info"),
    ]
)

layout = modelling.generate_layout(input_source=file_upload_component)


@callback(
    [
        Output("file-info", "children"),
        Output("file-info", "style"),
        Output("file-upload-store", "data"),
    ],
    [Input("file-upload", "contents"), Input("file-upload", "filename")],
)
def get_upload_data(
    contents: str, filename: str
) -> Tuple[str, dict, Optional[dict]]:
    """Extract and validate data from uploaded files.

    Args:
        contents (str): Base64-encoded string with the file's contents.
        filename (str): The name of the uploaded file.

    Returns:
        Tuple[str, dict, Optional[dict]]: file-info message, file-info style
        and the data-dict to store.
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
        if filename.endswith(".csv"):
            df = pd.read_csv(
                StringIO(file_content.decode("utf-8")), index_col=0
            )
        elif filename.endswith(".xls") or filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(file_content), index_col=0)
    except Exception as error:
        print(error)
        return (
            "There was an error processing the file.",
            {"color": "orangered"},
            None,  # No data to store
        )

    if (validation_error := process_upload(data=df)) is not None:
        return (
            validation_error,
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
