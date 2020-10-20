from ts_app.fit_time_series import TimeSeriesResults
import pandas as pd
import numpy as np


data = pd.Series(np.random.rand(50),
                 index=pd.date_range("2020-01-01", periods=50))
sample_results = TimeSeriesResults(data)


def testing_ts_prediction():
    """Check if the predictions have required properties."""
    # Each fitted model has a column
    assert list(sample_results.predictions.columns) == \
           ["Actual Data", "Predictions"]
    # Predictions should cover 60% of the data
    assert len(sample_results.predictions) == len(data) * 0.6


def testing_graphing_functions():
    """
    Check if graphs were plotted and set to their respective attributes.
    """
    assert "<!DOCTYPE svg PUBLIC" in sample_results.acf_pacf.getvalue()
    assert "<!DOCTYPE svg PUBLIC" in sample_results.lineplot.getvalue()
    assert "<!DOCTYPE svg PUBLIC" in sample_results.modelfit.getvalue()
    assert "<!DOCTYPE svg PUBLIC" in \
        sample_results.seasonal_decomposition.getvalue()
