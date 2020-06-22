from ts_functions import TimeSeriesGraphs, TimeSeriesPredictions
from ts_functions import clear_old_files
from glob import glob
import pandas as pd
import numpy as np


def testing_file_cleaning():
    # clear png files in default directory 'static/files'
    clear_old_files("png")
    assert len(glob("static/files/*.png", recursive=True)) == 0
    # creating sample png file
    with open("static/files/sample.png", "w") as file:
        file.write("...")
    assert len(glob("static/files/*.png", recursive=True)) == 1
    # removing created png file
    clear_old_files("png")
    assert len(glob("static/files/*.png", recursive=True)) == 0


data = pd.DataFrame(
    {"X": np.random.rand(50)}, index=pd.date_range("2020-01-01", periods=50)
)
clear_old_files("png")
predictions = TimeSeriesPredictions(data)
Graphs = TimeSeriesGraphs(data, predictions.results)


def testing_ts_prediction():
    # check if the models were fitted, and predictions were made
    assert all(
        predictions.results.columns == ["AR", "ARMA", "Exponential Smoothing"])
    assert len(predictions.results) == len(data) * 0.6  # default 'ratio'
    assert all(
     predictions.sample.columns == ["X", "AR", "ARMA", "Exponential Smoothing"]
    )
    assert len(predictions.sample) == 14  # default set in class definition


def testing_graphing_functions():
    # checking if the graphs were plotted
    assert "_acf_pacf_plots.png" in Graphs.acf_pacf
    assert "_line_plot.png" in Graphs.lineplot
    assert "-AR.png" in "".join(Graphs.modelfit)
    assert "_seasonal-decomp.png" in Graphs.seasonal_decomposition
