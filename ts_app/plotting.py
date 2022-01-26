import plotly.graph_objects as go
from pandas.core.series import Series
from plotly.subplots import make_subplots


def plot_ts_components(
    trend: Series, seasonal: Series, residuals: Series, file_name: str
) -> go.Figure:
    """Get subplots of time series components (trend, seasonal, residuals).

    Parameters
    ----------
    trend : Series
        Estimated trend component
    seasonal : Series
        Estimated seasonal component
    residuals : Series
        Estimated residual component
    file_name : str
        Data source info

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Subplots of time series compoments.
    """
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Trend", "Seasonal", "Residuals"),
    )
    fig.add_scatter(
        x=trend.index,
        y=trend,
        mode="lines",
        name="trend",
        line_color="navy",
        row=1,
        col=1,
    )
    fig.add_scatter(
        x=seasonal.index,
        y=seasonal,
        mode="lines",
        name="seasonal",
        line_color="seagreen",
        row=2,
        col=1,
    )
    fig.add_scatter(
        x=residuals.index,
        y=residuals,
        mode="lines",
        name="residuals",
        line_color="#ff3322",
        row=3,
        col=1,
    )
    fig.update_annotations(font_size=12)  # subplot titles are annotations
    fig.update_layout(
        font_family="serif",
        margin={"l": 10, "t": 80, "r": 10, "b": 10},
        paper_bgcolor="#eee",
        plot_bgcolor="#eee",
        showlegend=False,
        title=f"Seasonal Decomposition for {file_name}",
        title_font_size=14,
        xaxis1_showticklabels=True,
        xaxis2_showticklabels=True,
    )
    fig.update_traces(hovertemplate="%{x}: <b>%{y:,.4f}</b>", line_width=1)
    fig.update_yaxes(fixedrange=True)
    return fig


def plot_forecast(
    actual_data: Series,
    predictions: Series,
    forecast: Series,
    model_info: str,
    file_name: str,
) -> go.Figure:
    """Get a line-plot of the data, along with predicted values and a
    13-period forecast.

    Parameters
    ----------
    actual_data : Series
        The original/input data
    predictions : Series
        In-sample predicted values
    forecast : Series
        Out-of-sample predicted values
    model_info : str
        A description of the model's type and order
    file_name : str
        Input data source information.

    Returns
    -------
    plotly.graph_objs._figure.Figurego.Figure
        A line-plot of time series forecasting results.
    """
    fig = go.Figure(
        go.Scatter(
            y=actual_data,
            x=actual_data.index,
            mode="lines",
            name="actual data",
            line_color="#8888ff",
        ),
    )
    fig.add_scatter(
        x=predictions.index,
        y=predictions,
        mode="lines",
        name="predictions",
        line_color="navy",
    )
    fig.add_scatter(
        x=forecast.index,
        y=forecast,
        mode="lines",
        name="forecast",
        line_color="lime",
    )

    fig.update_layout(
        font_family="serif",
        hovermode="x unified",
        margin={"l": 10, "t": 80, "r": 10, "b": 10},
        paper_bgcolor="#eee",
        plot_bgcolor="#eee",
        title=f"An {model_info} model fitted on {file_name}",
        title_font_size=13,
    )
    fig.update_traces(hovertemplate="<b>%{y:,.4f}</b>", line_width=1)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    return fig
