from fit_time_series import TimeSeriesResults, clear_files
from glob import glob
import pandas as pd
import numpy as np


def testing_file_cleaning():
    """
    Check that the `clear_files` function actually clears specified files.
    """
    clear_files("png", filepath='static/files')
    with open("static/files/sample.png", "wb") as file:
        file.write(b"...")
    assert len(glob("static/files/*.png", recursive=True)) == 1
    clear_files("png")
    assert len(glob("static/files/*.png", recursive=True)) == 0


data = pd.Series(np.random.rand(50),
                 index=pd.date_range("2020-01-01", periods=50))
clear_files('svg')
sample_results = TimeSeriesResults(data)


def testing_ts_prediction():
    """Check if the predictions have required properties."""
    # Each fitted model has a column
    assert list(sample_results.predictions.columns) == \
           ["Actual Data", "Exponential Smoothing", "AR", "ARMA"]
    # Predictions should cover 60% of the data
    assert len(sample_results.predictions) == len(data) * 0.6


def testing_graphing_functions():
    """
    Check if graphs were plotted and set to their respective attributes.
    """
    assert "_acf_pacf_plots.svg" in sample_results.acf_pacf
    assert "_line_plot.svg" in sample_results.lineplot
    assert "_model-fit.svg" in "".join(sample_results.modelfit)
    assert "_seasonal-decomp.svg" in sample_results.seasonal_decomposition
