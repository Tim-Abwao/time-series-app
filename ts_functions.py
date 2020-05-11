import pandas as pd
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import os


def clear_old_files(extension, filepath="static/files/*."):
    """
    A utility function to remove old files of {extension} format, from the
    {filepath} folder.
    """
    old_files = glob.glob(filepath + extension, recursive=True)
    for file in old_files:
        os.remove(file)


class TimeSeriesPredictions:
    def __init__(self, data):
        self.results = self.fit_tsmodels(data)
        self.sample = self.sample(data)

    def fit_tsmodels(self, data, ratio=0.6) -> pd.DataFrame:
        """
        Fits AR, SARIMAX and Holt-Winters Exponential Smoothing models on the
        data(a pandas DataFrame). The predictions are returned as a dataframe
        with a column for each fitted model.
        """
        # setting prediction parameters
        n, index = len(data), data.index
        start = index[int(n * (1 - ratio))]
        end = index[-1]
        # Model fitting, and prediction
        pred1 = sm.tsa.AutoReg(data, lags=10).fit().predict(start, end)
        pred2 = sm.tsa.SARIMAX(data).fit().predict(start, end)
        pred3 = sm.tsa.ExponentialSmoothing(data).fit().predict(start, end)
        # returning results as a dataframe
        models_dict = {"AR": pred1, "SARIMAX": pred2, "Exponential Smoothing": pred3}
        return pd.DataFrame({**models_dict})

    def sample(self, data, size=14):
        return pd.concat([data, self.results], axis=1).round(2).tail(size)


class TimeSeriesGraphs:
    def __init__(self, data, results):
        self.file_folder = "static/files/"
        self.acf_pacf = self.plot_acf_pacf(data)
        self.lineplot = self.plot_line(data)
        self.modelfit = self.plot_model_fit(data, results)

    def plot_acf_pacf(self, data):
        """
        Produces the ACF & PACF graph, saving it as a png file, and returning
        it's path.
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
        Plots the data, saves it as a png image, and returns the save name.
        """
        plt.figure(figsize=(8, 4.5))
        plt.plot(data, color="navy")
        plt.xticks(rotation=90)
        plt.title("A line-plot of the data", size=15, pad=10)

        name = self.file_folder + str(datetime.now()) + "_line_plot.png"
        plt.savefig(name, transparent=True)
        return name

    def plot_model_fit(self, data, results):
        """
        Plots the original and predicted values for each time series model
        fitted, saves the graphs as images, and returns a list of graph
        paths.
        """
        names = []
        for model, values in results.iteritems():
            plt.figure(figsize=(8, 4.5))
            plt.plot(data, label="Original", color="navy")
            plt.plot(values, label="Modelled", color="aqua")
            plt.legend()
            plt.title(model + " Model Fit", size=15, pad=10)
            plt.xticks(rotation=90)
            name = self.file_folder + str(datetime.now()) + "-" + model + ".png"
            names.append(name)
            plt.savefig(name, transparent=True)
        return names
