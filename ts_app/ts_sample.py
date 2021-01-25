import pandas as pd
import numpy as np
from statsmodels.api import tsa
from datetime import date, timedelta


default_sample_params = {
    'start': date.today().isoformat(),
    'end': (date.today() + timedelta(days=30)).isoformat(),
    'frequencies': {"D": "Days",
                    "B": "Business days",
                    "w": "Weeks",
                    "M": "Months",
                    "Q": "Quarters"}
}


def create_arma_sample(ar_order, ma_order, size):
    """Get an ARMA sample of order (ar_order, ma_order) and given size.

    Parameters:
    ----------
    ar_order, ma_order, size: int
        Values for the desired AR order, MA order and sample size.

    Returns:
    -------
    An ARMA sample as a numpy array.
    """
    np.random.seed(1234)
    ar = np.linspace(1, -0.9, ar_order+1)
    ma = np.linspace(1, 0.9, ma_order+1)
    return tsa.ArmaProcess(ar, ma).generate_sample(size)


def process_sample_request(request):
    """
    Get sample data using parameters from the form in the given request.

    Parameters:
    ----------
    request: flask.Request
        A Flask request object with data from the sample-creation-form.

    Returns:
    -------
    A tuple, (error, data).
    """
    start = request.form["start_date"]
    stop = request.form["end_date"]
    frequency = request.form["frequency"]
    ar_order = int(request.form["ar_order"])
    ma_order = int(request.form["ma_order"])

    index = pd.date_range(start, stop, freq=frequency)
    n = len(index)

    if n < 30:
        error = f"""Please try again... The generated sample has
            {n} value(s) ({default_sample_params['frequencies'][frequency]})
            between {start} and {stop}, but the minimum sample size is set
            at 30."""
    else:
        error = None

    arma_sample = create_arma_sample(ar_order, ma_order, size=n)
    data = pd.Series(arma_sample, index=index, name="Sample")
    return error, data
