from typing import Tuple
import warnings
from datetime import date

import numpy as np
import pandas as pd
from statsmodels.api import tsa

# Ignore warnings from statsmodels. `ConvergenceWarning`s and `ValueWarning`s
# are all too frequent when fitting models on arbitrary data.
warnings.filterwarnings("ignore", module="statsmodels")


def create_arma_sample(
    ar_order: int = 1, ma_order: int = 1, size: int = 100
) -> pd.Series:
    """Get a random ARMA sample.

    Parameters
    ----------
    ar_order, ma_order, size : int
        Values for the desired AR order, MA order and sample size.

    Returns
    -------
    pandas.Series
        An ARMA sample.
    """
    ar_coeff = np.linspace(1, -0.9, ar_order + 1)  # arbitrary ar coefficients
    ma_coeff = np.linspace(1, 0.9, ma_order + 1)  # arbitrary ma coefficients
    sample = tsa.ArmaProcess(ar_coeff, ma_coeff).generate_sample(size)
    index = pd.date_range(start=date.today(), periods=size, freq="D")

    return pd.Series(sample, index=index, name="sample")


def fit_arima_model(
    data: pd.Series, ar_order: int = 1, diff: int = 0, ma_order: int = 1
) -> Tuple[pd.Series, pd.Series]:
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
    Tuple[pd.Series, pd.Series]
        In-sample predictions covering the latter 30% of the data, and a
        14-period out-of-sample forecast.
    """
    arima_model = tsa.arima.ARIMA(data, order=(ar_order, diff, ma_order)).fit()
    n = len(data)
    predictions = arima_model.predict(start=int(0.7 * n), end=n)
    forecast = arima_model.predict(start=n, end=n + 14)

    return predictions, forecast
