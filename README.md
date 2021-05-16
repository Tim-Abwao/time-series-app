# Time Series App

[![PyPI version](https://badge.fury.io/py/ts-app.svg)](https://badge.fury.io/py/ts-app)
[![Python application](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml/badge.svg)](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml)

A dashboard application to learn a little about, and apply *[Time Series][wiki_time_series] analysis* & *forecasting*.

You can create a sample, or upload a file, and interactively fit a time series model on it. 

The dashboard is built with [Dash][dash], and the time series models are fitted using [Statsmodels][statsmodels].

You can [try it out here][live-link].

[![screencast of the app](https://raw.githubusercontent.com/Tim-Abwao/time-series-app/master/dashboard.gif)][live-link]


## Installation

The easiest way to install the app is from [PyPI][pypi]:

```bash
pip install ts-app
```

You could also install it directly from the **GitHub** repository:

```bash
pip install https://github.com/tim-abwao/time-series-app/archive/main.tar.gz
```

## Basic Usage

The command `ts_app` launches the app:

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
