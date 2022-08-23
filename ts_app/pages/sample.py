import dash
from dash import Input, Output, callback, dcc, html
from ts_app.components import modelling
from ts_app.ts_functions import create_arma_sample

dash.register_page(__name__)

sample_param_dropdown = html.Div(
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

layout = modelling.generate_layout(input_source=sample_param_dropdown)


@callback(
    Output("sample-data-store", "data"),
    [Input("sample-ar", "value"), Input("sample-ma", "value")],
)
def get_sample(ar_order: int, ma_order: int) -> dict:
    """Generate a random ARMA sample with the provided parameters.

    Args:
        ar_order (int): AR order.
        ma_order (int): MA order.

    Returns:
        dict: The sample's description and data.
    """
    sample = create_arma_sample(ar_order, ma_order, size=365)

    return {
        "filename": f"an ARMA({ar_order}, {ma_order}) sample",
        "data": sample.to_json(),
    }
