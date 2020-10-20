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
        self._fit_arma_models()

    def _prediction_scope(self, coverage=0.6):
        """
        Get the time-range so that predictions span `coverage%`(60% default)
        of the data.
        """
        start = self.data.index[int((1 - coverage) * len(self.data))]
        end = self.data.index[-1]
        self.prediction_range = start, end

    def _fit_arma_models(self, max_ar=5, max_ma=5):
        """
        Fit time series models on the data, and get predictions as a dataframe.
        """
        arma_order = (list(range(1, max_ar)), 0, list(range(1, max_ma)))
        frequency = pd.infer_freq(self.data.index)

        arma_model = sm.tsa.arima.ARIMA(
            self.data, order=arma_order, freq=frequency
        ).fit()
        ts_predictions = arma_model.predict(14)

        self.model_summary = arma_model.summary().as_html()
        self.model_order = (arma_model.model_orders['ar'],
                            arma_model.model_orders['ma'])
        self.predictions = pd.DataFrame(
            {'Actual Data': self.data, "Predictions": ts_predictions}).dropna()


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
        Plot the original and predicted values, and save the graph as an svg
        file.
        """
        fig = Figure(figsize=(8, 4.5))
        ax = fig.subplots(1, 1)
        ax.plot(self.data, label="Original", color="navy")
        ax.plot(self.predictions['Predictions'], label="Modelled",
                color="aqua")
        ax.tick_params(axis='x', rotation=30)
        ax.set_title(f"An ARMA{self.model_order} model")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.legend()

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

    def _get_results(self):
        """
        Parse results as a dict to pass to the html templates.
        """
        ts_results = {
            'results': self.predictions,
            'sample': self.predictions.tail(14),
            'model_summary': self.model_summary,
            'graphs': {
                "acf&pacf": self.acf_pacf,
                "lineplot": self.lineplot,
                "modelfit": self.modelfit,
                "seasonal_decomposition": self.seasonal_decomposition,
            }
        }
        ts_results['totals'] = ts_results['sample'].sum().to_numpy(),
        self.results = ts_results
