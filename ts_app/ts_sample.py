import pandas as pd
import numpy as np
from statsmodels.api import tsa
from datetime import date


def create_arma_sample(ar_order, ma_order, size):
    """Get an ARMA sample of order (ar_order, ma_order) and given size.

    Parameters:
    ----------
    ar_order, ma_order, size: int
        Values for the desired AR order, MA order and sample size.

    Returns:
    -------
    An ARMA sample as a pandas Series.
    """
    ar = np.linspace(1, -0.9, ar_order+1)
    ma = np.linspace(1, 0.9, ma_order+1)
    sample = tsa.ArmaProcess(ar, ma).generate_sample(size)
    index = pd.date_range(start=date.today(), periods=size, freq='D')
    return pd.Series(sample, index=index)
