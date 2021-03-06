from statsmodels.api import tsa
from datetime import date
import pandas as pd
import numpy as np


def create_arma_sample(ar_order=1, ma_order=1, size=100):
    """Get a random ARMA sample of order (ar_order, ma_order) and given size.

    Parameters:
    ----------
    ar_order, ma_order, size: int
        Values for the desired AR order, MA order and sample size.

    Returns:
    -------
    An ARMA sample as a pandas Series.
    """
    ar = np.linspace(1, -0.9, ar_order+1)  # ar coefficients
    ma = np.linspace(1, 0.9, ma_order+1)  # ma coefficients
    sample = tsa.ArmaProcess(ar, ma).generate_sample(size)
    index = pd.date_range(start=date.today(), periods=size, freq='D')
    return pd.Series(sample, index=index)


def fit_arima_model(data, ar_order=1, ma_order=1, diff=0):
    """
    Fit an ARIMA model on the data and get predictions.

    Parameters:
    ----------
    data: pandas.Series
        A pandas series with a datettime index.
    ar_order, ma_order, diff: int
        Values for the AR order, MA order and level of Differencing
        respectively.
    """
    arima_model = tsa.arima.ARIMA(
        data, order=(ar_order, diff, ma_order), freq='D'
    ).fit()
    # In-sample prediction
    n = len(data)
    predictions = arima_model.predict(start=int(0.7*n), end=n)
    # Out-of sample forecast
    forecast = arima_model.predict(start=n, end=n+14)
    return predictions, forecast
