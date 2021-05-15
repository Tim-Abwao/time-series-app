import pandas as pd
from ts_app.ts_functions import create_arma_sample, fit_arima_model


def test_sample_creation():
    """Check if the sample creation function works as expected"""
    default_sample = create_arma_sample()
    assert isinstance(default_sample, pd.Series)
    assert default_sample.shape == (100,)
    assert default_sample.index.dtype == "datetime64[ns]"


def test_ts_prediction():
    """Check if the predictions have required properties."""
    data = create_arma_sample()
    predictions, forecast = fit_arima_model(data)
    assert predictions.shape == (31,)
    assert forecast.shape == (15,)
    assert predictions.index.dtype == forecast.index.dtype == "datetime64[ns]"
