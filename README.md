# Time Series App

A simple web app to learn a little about Time Series analysis and forecasting.

*\*Still under development\**.
To give it a try, [click here...](https://time-series-app.herokuapp.com)

## Running locally

### Prerequisites

[Python](https://www.python.org). Packages used include [statsmodels](https://www.statsmodels.org/stable/index.html), [flask](https://flask.palletsprojects.com/en/1.1.x/), [pandas](https://pandas.pydata.org) and [NumPy](https://numpy.org).

### Getting started

Fetching necessary files:

```bash
git clone https://github.com/Tim-Abwao/time-series-app.git
cd time-series-app
```

Setting up a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
pip install -U pip
pip install requirements.txt
```

Starting the app:

```bash
python app.py
```

Afterwards, browse to [localhost:5000](https://127.0.0.1:5000) to interact with the web app.
