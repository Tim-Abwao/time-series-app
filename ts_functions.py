import pandas as pd
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime
from glob import glob
import os
import matplotlib

matplotlib.rcParams["figure.autolayout"] = True
matplotlib.rcParams["backend"] = "Agg"
matplotlib.rcParams["legend.frameon"] = True


def clear_old_files(extension, filepath="static/files/*."):
    """
    A utility function to remove old files of {extension} format, from the
    {filepath} folder.
    """
    old_files = glob(filepath + extension, recursive=True)
    for file in old_files:
        os.remove(file)


class TimeSeriesPredictions:
    def __init__(self, data):
        self.results = self.fit_tsmodels(data)
        self.sample = self.sample(data)

    def fit_tsmodels(self, data, ratio=0.6) -> pd.DataFrame:
        """
        Fits AR, and Holt-Winters Exponential Smoothing models on the
        data(a pandas DataFrame). The predictions are returned as a dataframe
        with a column for each fitted model.
        """
        # setting prediction parameters
        n, index = len(data), data.index
        start = index[int(n * (1 - ratio))]
        end = index[-1]
        # Model fitting, and prediction
        model1 = sm.tsa.AutoReg(data, lags=10).fit().predict(start, end)
        model2 = (
            sm.tsa.ExponentialSmoothing(data, trend="additive", seasonal="additive")
            .fit()
            .predict(start, end)
        )
        # returning results as a dataframe
        models_dict = {"AR": model1, "Exponential Smoothing": model2}
        return pd.DataFrame({**models_dict})

    def sample(self, data, size=14) -> pd.DataFrame:
        """
        Creates a sample, a dataframe with the original and modelled data.
        This will be displayed as the table in the results page.
        """

        return pd.concat([data, self.results], axis=1).round(2).tail(size)


class TimeSeriesGraphs:
    def __init__(self, data, results):
        self.file_folder = "static/files/"
        self.acf_pacf = self.plot_acf_pacf(data)
        self.lineplot = self.plot_line(data)
        self.modelfit = self.plot_model_fit(data, results)
        self.seasonal_decomposition = self.plot_seanonal_decomposition(data)
        self.terminate()

    def plot_acf_pacf(self, data):
        """
        Produces the ACF & PACF graph, saving it as a png file, and returning
        it's location(name).
        """
        fig = plt.figure(figsize=(8, 6))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        plot_acf(data.values, ax=ax1, color="navy")
        plot_pacf(data.values, ax=ax2, color="navy")

        name = self.file_folder + str(datetime.now()) + "_acf_pacf_plots.png"
        plt.savefig(name, transparent=True)

        return name

    def plot_line(self, data):
        """
        Plots the data, saves it as a png file, and returns the file location.
        """
        plt.figure(figsize=(8, 4.5))
        plt.plot(data, color="navy")
        plt.xticks(rotation=30)
        plt.title("A line-plot of the data", size=15, pad=10)
        name = self.file_folder + str(datetime.now()) + "_line_plot.png"
        plt.savefig(name, transparent=True)

        return name

    def plot_model_fit(self, data, results):
        """
        Plots the original and predicted values for each time series model
        fitted, saves the graphs as png files, and returns a list of file
        locations(names).
        """
        names = []
        for model, values in results.iteritems():
            plt.figure(figsize=(8, 4.5))
            plt.plot(data, label="Original", color="navy")
            plt.plot(values, label="Modelled", color="aqua")
            plt.title(model + " Model Fit", size=15, pad=10)
            plt.xticks(rotation=30)
            name = self.file_folder + str(datetime.now()) + "-" + model + ".png"
            names.append(name)
            plt.savefig(name, transparent=True)

        return names

    def plot_seanonal_decomposition(self, data):
        """
        Performs basic seasonal decomposition, plots the various components,
        saves them as a png file, and returns their location.
        """
        name = self.file_folder + str(datetime.now()) + "_seasonal-decomposition.png"
        sm.tsa.seasonal_decompose(data).plot().autofmt_xdate()
        plt.savefig(name, transparent=True)

        return name

    def terminate(self):
        plt.close("all")
