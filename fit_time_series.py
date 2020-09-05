import pandas as pd
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.tsa.arima_process import arma_generate_sample
import statsmodels.api as sm
import matplotlib
from datetime import datetime
from glob import glob
import numpy as np
import os

# matplotlib configurations
matplotlib.use("Agg")
matplotlib.rcParams["figure.autolayout"] = True
matplotlib.rcParams["legend.frameon"] = True
plt = matplotlib.pyplot


def clear_files(extension, filepath="static/files/"):
    """
    Delete files of specified format from the supplied directory.
    """
    files = glob("".join([filepath, "*.", extension]), recursive=True)
    [os.remove(file) for file in files]


def create_arma_sample(ar_order, ma_order, size):
    """Get an ARMA sample of order (ar_order, ma_order) and given size."""
    np.random.seed(123)
    ar = np.linspace(-0.9, 0.9, ar_order)
    ma = np.linspace(-1, 1, ma_order)
    arma_sample = arma_generate_sample(
        ar, ma, size, scale=100, distrvs=np.random.standard_normal
    )
    return arma_sample


class TimeSeriesPredictions:
    """
    Fit various time series models and make predictions, using `statsmodels`.
    """

    def __init__(self, data):
        self.data = data
        self._prediction_scope()
        self._fit_ts_models()

    def _prediction_scope(self, coverage=0.6):
        """
        Get the time-range so that predictions span `coverage%`(60% default)
        of the data.
        """
        start = self.data.index[int((1 - coverage) * len(self.data))]
        end = self.data.index[-1]
        self.prediction_range = start, end

    def _fit_ts_models(self):
        """
        Fit time series models on the data, and get predictions as a dataframe.
        """
        scope = self.prediction_range
        ts_predictions = {
            "Exponential Smoothing": (sm.tsa.ExponentialSmoothing(
                                        self.data, trend="add", seasonal="add"
                                        ).fit()
                                         .predict(*scope)),
            "AR": (sm.tsa.AutoReg(self.data, lags=10)
                     .fit()
                     .predict(*scope))
            }
        # Searching for appropriate ARMA order
        try:
            arma_ic = sm.tsa.arma_order_select_ic(self.data, ic="bic",
                                                  trend="nc",
                                                  fit_kw={"dist": 0})
            # Set ARMA order order >= (1, 1)
            arma_order = max(arma_ic.bic_min_order, (1, 1))
            ts_predictions['ARMA'] = (sm.tsa.ARMA(self.data, arma_order)
                                        .fit(disp=0)
                                        .predict(*scope))
        except ValueError:  # raised if above arma model fails to converge
            ts_predictions['ARMA'] = (sm.tsa.ARMA(self.data, (1, 1))
                                        .fit(disp=0)
                                        .predict(*scope))

        self.predictions = pd.DataFrame({'Actual Data': self.data,
                                         **ts_predictions}).dropna()


class TimeSeriesResults(TimeSeriesPredictions):
    """
    Plot graphs to asses time series predictions.
    """

    def __init__(self, data):
        super().__init__(data)
        self.save_dir = "static/files/"
        self._plot_acf_pacf()
        self._plot_line()
        self._plot_model_fit()
        self._plot_seanonal_decomposition()
        self._terminate()

    def _plot_acf_pacf(self):
        """
        Plot ACF & PACF graphs of the data, and save them as an svg file.
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        plot_acf(self.data.values, ax=ax1, color="navy")
        plot_pacf(self.data.values, ax=ax2, color="navy")
        self.acf_pacf = self._save_graph("acf_pacf_plots.svg")

    def _plot_line(self):
        """
        Plot the data, and save the graph as an svg file.
        """
        plt.figure(figsize=(8, 4))
        plt.plot(self.data, color="navy")
        plt.xticks(rotation=30)
        plt.title("A line-plot of the data", size=15, pad=10)
        self.lineplot = self._save_graph("line_plot.svg")

    def _plot_model_fit(self):
        """
        Plot the original and predicted values for each time series model
        fitted, and save the graph as an svg file.
        """
        fig, axs = plt.subplots(3, 1, figsize=(8, 16))
        predictions = self.predictions.drop('Actual Data', axis=1)
        for idx, model_values in enumerate(predictions.iteritems()):
            axs[idx].plot(self.data, label="Original", color="navy")
            axs[idx].plot(model_values[1], label="Modelled", color="aqua")
            axs[idx].set_title(model_values[0] + " Model Fit", size=15, pad=15)
            axs[idx].set_xticklabels(model_values[1].index, rotation=60)

        plt.legend()
        self.modelfit = self._save_graph("model-fit.svg")

    def _plot_seanonal_decomposition(self):
        """
        Perform seasonal decomposition with LOESS, plot the various components,
        and save the graphs as an svg file.
        """
        sm.tsa.STL(self.data).fit().plot().autofmt_xdate()
        self.seasonal_decomposition = self._save_graph("seasonal-decomp.svg")

    def _save_graph(self, name):
        """Give time-stamped names to matplotlib graphs, and save them."""
        filepath = f"{self.save_dir}{str(datetime.now())}_{name}"
        plt.savefig(filepath, transparent=True)
        return filepath

    def _terminate(self):
        """Closes all lingering `matplotlib.pyplot` figures."""

        plt.close("all")
