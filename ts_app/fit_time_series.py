import statsmodels.api as sm


def fit_arima_model(data, ar_order=1, ma_order=1, diff=0):
    """
    Fit an ARIMA model and get predictions as a dataframe.
    """
    n = len(data)
    arima_model = sm.tsa.arima.ARIMA(
        data, order=(ar_order, diff, ma_order), freq='D'
    ).fit()
    # In-sample predictions
    predictions = arima_model.predict(start=int(0.7*n), end=n)
    # Out-of sample forecast
    forecast = arima_model.predict(start=n, end=n+14)
    summary = arima_model.summary().as_html()
    return predictions, forecast, summary
