import pandas as pd
from pandas.api.types import is_datetime64_dtype
from ts_app.ts_functions import create_arma_sample, fit_arima_model


def test_default_sample_creation():
    default_sample = create_arma_sample()

    assert isinstance(default_sample, pd.Series)
    assert default_sample.shape == (100,)
    assert is_datetime64_dtype(default_sample.index)


def test_specified_sample_creation():
    default_sample = create_arma_sample(ar_order=2, ma_order=2, size=200)

    assert isinstance(default_sample, pd.Series)
    assert default_sample.shape == (200,)
    assert is_datetime64_dtype(default_sample.index)


def test_ts_prediction():
    data = create_arma_sample()
    predictions, forecast = fit_arima_model(data)

    assert predictions.shape == (31,)
    assert forecast.shape == (15,)
    assert is_datetime64_dtype(predictions.index)
