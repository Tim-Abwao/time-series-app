from io import StringIO
import matplotlib
from matplotlib.figure import Figure
import pandas as pd
import statsmodels.api as sm


# matplotlib configurations
matplotlib.use('svg')
matplotlib.rcParams["figure.autolayout"] = True
matplotlib.rcParams["legend.frameon"] = True


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
            "Exponential Smoothing": (sm.tsa.ExponentialSmoothing(self.data)
                                        .fit()
                                        .predict(*scope)),
            "AR": (sm.tsa.AutoReg(self.data, lags=10)
                     .fit()
                     .predict(*scope))
            }

        # Searching for appropriate ARMA order
        p, q = sm.tsa.arma_order_select_ic(
                      self.data, ic="bic", max_ar=4, max_ma=4,
                    ).bic_min_order
        arma_order = (list(range(1, p+1)), 0, list(range(1, q+1)))
        ts_predictions['ARMA'] = (sm.tsa.arima.ARIMA(
                                        self.data, order=arma_order)
                                    .fit()
                                    .predict(*scope))

        self.predictions = pd.DataFrame({'Actual Data': self.data,
                                         **ts_predictions}).dropna()


class TimeSeriesResults(TimeSeriesPredictions):
    """
    Fit time series models, make predictions, and plot graphs to asses results.
    """

    def __init__(self, data):
        super().__init__(data)
        self._plot_acf_pacf()
        self._plot_line()
        self._plot_model_fit()
        self._plot_seanonal_decomposition()
        self._terminate()
        self._get_results()

    def _plot_acf_pacf(self):
        """
        Plot ACF & PACF graphs of the data, and save them as an svg file.
        """
        fig = Figure(figsize=(8, 6))
        ax1, ax2 = fig.subplots(2, 1)
        sm.graphics.tsa.plot_acf(self.data.values, ax=ax1, color="navy")
        sm.graphics.tsa.plot_pacf(self.data.values, lags=12, ax=ax2,
                                  color="navy")
        self.acf_pacf = self._save_graph(fig)

    def _plot_line(self):
        """
        Plot the data, and save the graph as an svg file.
        """
        fig = Figure(figsize=(8, 4))
        ax = fig.subplots()
        ax.plot(self.data, color="navy")
        ax.tick_params(axis='x', rotation=30)
        ax.set_title("A line-plot of the data", size=15, pad=10)
        self.lineplot = self._save_graph(fig)

    def _plot_model_fit(self):
        """
        Plot the original and predicted values for each time series model
        fitted, and save the graph as an svg file.
        """
        fig = Figure(figsize=(8, 16))
        axs = fig.subplots(3, 1)
        predictions = self.predictions.drop('Actual Data', axis=1)
        for idx, model_values in enumerate(predictions.iteritems()):
            axs[idx].plot(self.data, label="Original", color="navy")
            axs[idx].plot(model_values[1], label="Modelled", color="aqua")
            axs[idx].set_title(model_values[0] + " Model Fit", size=15, pad=15)
            axs[idx].tick_params(axis='x', rotation=60)

        self.modelfit = self._save_graph(fig)

    def _plot_seanonal_decomposition(self):
        """
        Perform seasonal decomposition with LOESS, plot the various components,
        and save the graphs as an svg file.
        """
        fig = sm.tsa.STL(self.data).fit().plot()
        fig.autofmt_xdate()
        self.seasonal_decomposition = self._save_graph(fig)

    @staticmethod
    def _save_graph(fig):
        """Give time-stamped names to matplotlib graphs, and save them."""
        file = StringIO()
        fig.savefig(file, transparent=True, format='svg')
        return file

    def _terminate(self):
        """Closes all lingering `matplotlib.pyplot` figures."""

        # fig.close("all")

    def _get_results(self):
        """
        Parse results as a dict to pass to the html templates.
        """
        ts_results = {
            'results': self.predictions,
            'sample': self.predictions.tail(14),
            'graphs': {
                "acf&pacf": self.acf_pacf,
                "lineplot": self.lineplot,
                "model_fit": self.modelfit,
                "seasonal_decomposition": self.seasonal_decomposition
            }
        }
        ts_results['totals'] = ts_results['sample'].sum().to_numpy(),
        self.results = ts_results
