import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ts_app.dash_app import app
from ts_app.ts_functions import create_arma_sample

input_layout = html.Div(
    id="sample-params",
    className="param-input",
    children=[
        html.H3("Sample parameters"),
        # AR order dropdown
        html.Label("AR Order", htmlFor="sample-ar"),
        dcc.Dropdown(
            id="sample-ar",
            clearable=False,
            placeholder="AR order",
            searchable=False,
            value=1,
            options=[{"label": f"{i}", "value": i} for i in range(1, 5)],
        ),
        # MA order dropdown
        html.Label("MA Order", htmlFor="sample-ma"),
        dcc.Dropdown(
            id="sample-ma",
            clearable=False,
            placeholder="MA order",
            searchable=False,
            value=1,
            options=[{"label": f"{i}", "value": i} for i in range(1, 5)],
        ),
    ],
)


@app.callback(
    Output("sample-data-store", "data"),
    [Input("sample-ar", "value"), Input("sample-ma", "value")],
)
def get_sample(ar_order: int, ma_order: int) -> dict:
    """Create an ARMA sample with the given parameters.

    Parameters
    ----------
    ar_order, ma_order : int
        AR order and MA order respectively.

    Returns
    -------
    dict
        The sample's name and data.
    """
    sample = create_arma_sample(ar_order, ma_order, size=150)

    return {
        "filename": f"an ARMA({ar_order}, {ma_order}) sample",
        "data": sample.to_json(),
    }
