import pandas as pd
import numpy as np
from statsmodels.api import tsa
from datetime import date, timedelta


default_sample_params = {'start': date.today().isoformat(),
                         'end': (date.today()
                                 + timedelta(days=30)).isoformat(),
                         'frequencies': {"D": "Days",
                                         "B": "Business days",
                                         "w": "Weeks",
                                         "M": "Months",
                                         "Q": "Quarters",
                                         "Y": "Years"
                                         }
                         }


def create_arma_sample(ar_order, ma_order, size):
    """Get an ARMA sample of order (ar_order, ma_order) and given size."""
    np.random.seed(123)
    ar = np.linspace(-0.9, 0.9, ar_order)
    ma = np.linspace(-1, 1, ma_order)
    arma_sample = tsa.arma_generate_sample(
        ar, ma, size, scale=100, distrvs=np.random.standard_normal
    )
    return arma_sample


def process_sample_request(request):
    """
    Get sample data using parameters from the form in the given request.
    """
    error = None
    data = None
    try:
        start = request.form["start_date"]
        stop = request.form["end_date"]
        frequency = request.form["frequency"]
        ar_order = int(request.form["ar_order"])
        ma_order = int(request.form["ma_order"])
    except KeyError:
        start = default_sample_params['start']
        stop = default_sample_params['end']
        frequency, ar_order, ma_order = "D", 1, 1

    index = pd.date_range(start, stop, freq=frequency)
    n = len(index)
    if n < 30:
        error = f"""Please try again... The generated sample has
            {n} value(s) ({default_sample_params['frequencies'][frequency]})
            between {start} and {stop}, but the minimum sample size is set
            at 30."""

    arma_sample = create_arma_sample(ar_order, ma_order, size=n)
    data = pd.Series(arma_sample, index=index, name="Sample")

    return error, data
