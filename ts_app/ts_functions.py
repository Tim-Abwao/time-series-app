import warnings
from datetime import date

import numpy as np
import pandas as pd
from statsmodels.api import tsa

# Ignore warnings from statsmodels. `ConvergenceWarning`s and `ValueWarning`s
# are all too frequent when fitting models on arbitrary data.
warnings.filterwarnings("ignore", module="statsmodels")


def create_arma_sample(ar_order=1, ma_order=1, size=100):
    """Get a random ARMA sample.

    Parameters
    ----------
    ar_order, ma_order, size : int
        Values for the desired AR order, MA order and sample size.

    Returns
    -------
    An ARMA sample as a pandas Series.
    """
    ar_coeff = np.linspace(1, -0.9, ar_order + 1)  # arbitrary ar coefficients
    ma_coeff = np.linspace(1, 0.9, ma_order + 1)  # arbitrary ma coefficients
    sample = tsa.ArmaProcess(ar_coeff, ma_coeff).generate_sample(size)
    index = pd.date_range(start=date.today(), periods=size, freq="D")

    return pd.Series(sample, index=index, name="sample")


def fit_arima_model(data, ar_order=1, diff=0, ma_order=1):
    """Fit an ARIMA model on the data and get predictions.

    Parameters
    ----------
    data : pandas.Series
        The data to model, indexed by date.
    ar_order, ma_order, diff : int
        Values for the AR order, MA order and degree of Differencing
        respectively.

    Returns
    -------
    In-sample predictions covering the latter 30% of the data, and a 14-period
    out-of-sample forecast.
    """
    # Fit an ARIMA model
    arima_model = tsa.arima.ARIMA(data, order=(ar_order, diff, ma_order)).fit()
    # Get in-sample predictions
    n = len(data)
    predictions = arima_model.predict(start=int(0.7 * n), end=n)
    # Get forecast
    forecast = arima_model.predict(start=n, end=n + 14)

    return predictions, forecast
