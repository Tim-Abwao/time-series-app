# Time Series App

[![PyPI version](https://badge.fury.io/py/ts-app.svg)](https://badge.fury.io/py/ts-app)
[![Python application](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml/badge.svg)](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml)

A dashboard application to help learn a little about, and apply *[Time Series][wiki_time_series] analysis* & *forecasting* concepts.

You can create a sample, or upload a file, and interactively fit a time series model on it.

The dashboard is built with [Dash][dash], and the time series models are fitted using [Statsmodels][statsmodels].

You can [try it out here][live-link], courtesy of [Render][render].

>**NOTE:** Free-hosted apps on *Render* might take a while to load since they are shut down when not in use.

![screencast of the app](https://raw.githubusercontent.com/Tim-Abwao/time-series-app/master/screencast.gif)

## Installation

The easiest way to get the app is from [PyPI][pypi]:

```bash
pip install ts-app
```

## Basic Usage

The command `ts_app` launches the app:

```bash
$ ts_app -h
usage: ts_app [-h] [-p PORT] [--host HOST] [--no-browser]

A simple dashboard application to learn time series basics and interactively fit ARIMA models.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  The TCP port on which to listen (default: 8000).
  --host HOST           A host-name or IP address (default: 'localhost').
  --no-browser          Avoid openning a browser tab or window.
```

You can also start the app from an interactive session:

```python
>>> import ts_app
>>> ts_app.run_app()
```

Afterwards, press `CTRL` + `C` to stop the server.

[wiki_time_series]: https://en.wikipedia.org/wiki/Time_series
[live-link]: https://time-series-app.onrender.com
[dash]: https://dash.plotly.com/
[render]: https://render.com/
[statsmodels]: https://www.statsmodels.org/stable/index.html
[pypi]:  https://pypi.org/project/ts-app/
