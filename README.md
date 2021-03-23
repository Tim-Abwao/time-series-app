# Time Series App

[![PyPI version](https://badge.fury.io/py/ts-app.svg)](https://badge.fury.io/py/ts-app)
[![Python application](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml/badge.svg)](https://github.com/Tim-Abwao/time-series-app/actions/workflows/python-app.yml)

A simple web app to learn a little about *[Time Series][1] analysis* and *forecasting*.

You can create a sample, or upload a file, and interactively fit a time series model on it. To give it a try, [click here...][2]

[![screencast of the app](https://raw.githubusercontent.com/Tim-Abwao/time-series-app/master/dashboard.gif)][2]

## Installation

The easiest way to install the app is from [PyPI][3] using:

```bash
pip install ts-app
```

You can then start it using the command

```bash
ts_app
```

or even

```bash
python -m ts_app
```

Press `CTRL` + `C` to stop it.

You can also start the app from an interactive session:

```python
>>> import ts_app
>>> ts_app.run_app()
```

## Manual set up

### 1. Using a virtual environment

You'll need [Python][4] 3.8 and above. Packages used include [statsmodels][5], [flask][6], [dash][7], [pandas][8] and [NumPy][9].

1. Fetch the necessary files:

    ```bash
    git clone https://github.com/Tim-Abwao/time-series-app.git
    cd time-series-app
    ```

2. Create the virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    ```

3. Start the app:

    You can use the convenient `run.sh` script, or `waitress`:

    ```bash
    waitress-serve --listen=127.0.0.1:8000 ts_app:server
    ```

    then browse to [localhost:8000](http://127.0.0.1:8000) to interact with the web app.

    Afterwards, use `CTRL` + `C` to stop it.

### 2. Using Docker

You'll need [Docker][10].

1. Fetch the necessary files, just as above:

    ```bash
    git clone https://github.com/Tim-Abwao/time-series-app.git
    cd time-series-app
    ```

2. Build an image for the app and run it in a container,

    ```bash
    docker build --tag ts_app .
    docker run --name ts -d -p 8000:8000 --rm  ts_app
    ```

    in which case the app will be running at <http://0.0.0.0:8000>.

    Afterwards, use

    ```bash
    docker stop ts
    ```

    to terminate it.

[1]: https://en.wikipedia.org/wiki/Time_series
[2]: https://time-series-app.herokuapp.com
[3]: https://pypi.org/project/ts-app/
[4]: https://www.python.org "The Python programming language"
[5]: https://www.statsmodels.org/stable/index.html
[6]: https://flask.palletsprojects.com/en/1.1.x/
[7]: https://dash.plotly.com/
[8]: https://pandas.pydata.org
[9]: https://numpy.org
[10]: https://www.docker.com/
