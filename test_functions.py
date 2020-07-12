from ts_functions import TimeSeriesResults
from ts_functions import clear_old_files
from glob import glob
import pandas as pd
import numpy as np


def testing_file_cleaning():
    """
    Checks that the `clear_old_files` function actually clears specified files.
    """
    # clearing any existing png files in the default directory 'static/files'
    clear_old_files("png")
    # checking that all png files there are gone
    assert len(glob("static/files/*.png", recursive=True)) == 0
    # creating a sample png file
    with open("static/files/sample.png", "wb") as file:
        file.write(b"...")
    assert len(glob("static/files/*.png", recursive=True)) == 1
    # removing created png file
    clear_old_files("png")
    assert len(glob("static/files/*.png", recursive=True)) == 0


data = pd.Series(np.random.rand(50),
                 index=pd.date_range("2020-01-01", periods=50))
sample_results = TimeSeriesResults(data)


def testing_ts_prediction():
    """
    Checks if the `TimeSeriesPredictions` class methods make and save the
    required predictions.
    """
    assert all(sample_results.results.columns ==
               ["Actual Data", "AR", "ARMA", "Exponential Smoothing"])
    # ensuring the results cover 60% of the data (default defined in the model
    # fitting function)
    assert len(sample_results.results) == len(data) * 0.6
    # checking the sample's properties
    assert all(sample_results.sample.columns ==
               ["Actual Data", "AR", "ARMA", "Exponential Smoothing"])
    assert len(sample_results.sample) == 14  # 14 is the default sample size


def testing_graphing_functions():
    """
    Checks if the TimeSeriesGraphs class methods run successfully. If they do
    graphs would be plotted, then graph names would be returned and set to
    their respective attribues.
    """
    assert "_acf_pacf_plots.png" in sample_results.acf_pacf
    assert "_line_plot.png" in sample_results.lineplot
    assert "-AR.png" in "".join(sample_results.modelfit)
    assert "_seasonal-decomp.png" in sample_results.seasonal_decomposition
