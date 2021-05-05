# Time Series App

[![PyPI version](https://badge.fury.io/py/ts-app.svg)](https://badge.fury.io/py/ts-app)
[![Python application](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml/badge.svg)](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml)

A simple web app to learn a little about *[Time Series][wiki_time_series] analysis* and *forecasting*.

You can create a sample, or upload a file, and interactively fit a time series model on it. To give it a try, [click here...][live-link]

[![screencast of the app](https://raw.githubusercontent.com/Tim-Abwao/time-series-app/master/dashboard.gif)][live-link]

The dashboard is built with [Dash][dash], and the time series models are fitted using [Statsmodels][statsmodels].

## Installation

The easiest way to install the app is from [PyPI][pypi], using:

```bash
pip install ts-app
```

You could also install it directly from the **GitHub** repository using:

```bash
pip install https://github.com/tim-abwao/time-series-app/archive/main.tar.gz
```

## Basic Usage

You can use the command `ts_app` to launch the app.

```bash
ts_app
```

You can also start the app from an interactive session:

```python
>>> import ts_app
>>> ts_app.run_app()
```

Afterwards, press `CTRL` + `C` to stop it.

[wiki_time_series]: https://en.wikipedia.org/wiki/Time_series
[live-link]: https://time-series-app.herokuapp.com
[dash]: https://dash.plotly.com/
[statsmodels]: https://www.statsmodels.org/stable/index.html
[pypi]:  https://pypi.org/project/ts-app/
