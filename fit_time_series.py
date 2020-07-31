import pandas as pd
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import statsmodels.api as sm
import matplotlib
from datetime import datetime
from glob import glob
import os

# matplotlib configurations
matplotlib.use("Agg")
matplotlib.rcParams["figure.autolayout"] = True
matplotlib.rcParams["figure.figsize"] = (8, 4.5)
matplotlib.rcParams["legend.frameon"] = True
plt = matplotlib.pyplot


def clear_files(extension, filepath="static/files/"):
    """
    Deletes files of {extension} format, from the {filepath} directory.
    """
    files = glob("".join([filepath, "*.", extension]), recursive=True)
    for file in files:
        os.remove(file)


class TimeSeriesPredictions:
    """A class of methods for fitting time series models"""

    def _prediction_scope(self, data, coverage=0.6):
        """
        Returns the prediction start & end dates that cover {coverage} * 100%
        of the data (60% by default).
        """
        n_rows, index = len(data), data.index
        start = index[int((1 - coverage) * n_rows)]
        end = index[-1]
        return start, end

    def _fit_ts_models(self, data):
        """This fits various time series models on the data."""

        # AR model
        ar_model = sm.tsa.AutoReg(data, lags=10).fit()

        # Holt-Winters Exponential Smoothing model
        holtwint_exp_model = (
          sm.tsa.ExponentialSmoothing(data, trend="add", seasonal="add")
          .fit()
        )

        # ARMA model
        try:  # Searching for an appropriate ARMA order
            arma_ic = sm.tsa.arma_order_select_ic(
                data, ic="bic", trend="nc", fit_kw={"dist": 0}
            )
            arma_order = max(arma_ic.bic_min_order, (1, 1))
            arma_model = sm.tsa.ARMA(data, arma_order).fit(disp=0)
        except ValueError:  # raised if above arma model dfails to converge
            # Explicitly attempt to fit an ARMA (1,1) model
            arma_model = sm.tsa.ARMA(data, (1, 1)).fit(disp=0)

        ts_models = {"AR": ar_model, "ARMA": arma_model,
                     "Exponential Smoothing": holtwint_exp_model}
        return ts_models

    def _get_predictions(self, data) -> pd.DataFrame:
        """Obtains forecast results for the fitted time series models."""

        predictions = {}
        models = self._fit_ts_models(data)

        for name, model in models.items():
            predicted_values = model.predict(*self._prediction_scope(data))
            predictions[name] = predicted_values

        return pd.DataFrame({'Actual Data': data, **predictions}).dropna()


class TimeSeriesResults(TimeSeriesPredictions):
    """
    The class of methods to compute and store time series forecasting results
    """

    def __init__(self, data):
        self.results = super()._get_predictions(data).round(2)
        self.sample = self.results.tail(14)
        self.file_folder = "static/files/"
        self.acf_pacf = self._plot_acf_pacf(data)
        self.lineplot = self._plot_line(data)
        self.modelfit = self._plot_model_fit(data, self.results)
        self.seasonal_decomposition = self._plot_seanonal_decomposition(data)
        self._terminate()

    def _plot_acf_pacf(self, data):
        """
        Produces the ACF & PACF graphs, saving them as a png file, and
        returning their location.
        """
        fig = plt.figure(figsize=(8, 6))
        ax1, ax2 = fig.add_subplot(211), fig.add_subplot(212)
        plot_acf(data.values, ax=ax1, color="navy")
        plot_pacf(data.values, ax=ax2, color="navy")
        name = self._file_namer("acf_pacf_plots.png")
        plt.savefig(name, transparent=True)

        return name

    def _plot_line(self, data):
        """
        Plots the data, saves the graph as a png file, and returns its
        location(name).
        """
        plt.figure()
        plt.plot(data, color="navy")
        plt.xticks(rotation=30)
        plt.title("A line-plot of the data", size=15, pad=10)
        name = self._file_namer("line_plot.png")
        plt.savefig(name, transparent=True)

        return name

    def _plot_model_fit(self, data, results):
        """
        Plots the original and predicted values for each time series model
        fitted, saves the graphs as a png file, and returns its locations
        (name).
        """
        fig = plt.figure(figsize=(8, 18))
        i = 1
        for model, values in results.drop('Actual Data', axis=1).iteritems():
            fig.add_subplot(3, 1, i)
            plt.plot(data, label="Original", color="navy")
            plt.plot(values, label="Modelled", color="aqua")
            plt.title(model + " Model Fit", size=15, pad=15)
            plt.xticks(rotation=30)
            plt.legend()
            i += 1

        name = self._file_namer("model-fit.png")
        plt.savefig(name, transparent=True)

        return name

    def _plot_seanonal_decomposition(self, data):
        """
        Performs basic seasonal decomposition, plots the various components,
        saves the graphs as a png file, and returns its location(name).
        """
        # Seasonal decomposition with LOESS
        sm.tsa.STL(data).fit().plot().autofmt_xdate()
        name = self._file_namer("seasonal-decomp.png")
        plt.savefig(name, transparent=True)

        return name

    def _file_namer(self, name):
        """Names files such that they get saved in `self.file_folder`"""
        return "".join(
            [self.file_folder, str(datetime.now()), "_", name])

    def _terminate(self):
        """Closes all lingering `matplotlib.pyplot` `Figure`s"""

        plt.close("all")
