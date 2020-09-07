import pandas as pd
from ts_app.fit_time_series import create_arma_sample
from datetime import date, timedelta


sample_parameters = {'start': date.today().isoformat(),
                     'end': (date.today() + timedelta(days=30)).isoformat(),
                     'frequencies': {"D": "Days",
                                     "B": "Business days",
                                     "w": "Weeks",
                                     "M": "Months",
                                     "Q": "Quarters",
                                     "Y": "Years"
                                     }
                     }


def process_sample(request):
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
        start, stop = sample_parameters['start'], sample_parameters['end']
        frequency, ar_order, ma_order = "D", 1, 1

    index = pd.date_range(start, stop, freq=frequency)
    n = len(index)
    if n < 30:
        error = f"""Please try again... The generated sample has
            {n} value(s) ({sample_parameters['frequencies'][frequency]})
            between {start} and {stop}, but the minimum sample size is set
            at 30."""

    arma_sample = create_arma_sample(ar_order, ma_order, size=n)
    data = pd.Series(arma_sample, index=index, name="Sample")

    return error, data
