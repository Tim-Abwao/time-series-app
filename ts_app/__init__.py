from flask import Flask, render_template, request
from ts_app.fit_time_series import TimeSeriesResults as TS
from ts_app.file_upload import process_upload
from ts_app.ts_sample import default_sample_params, process_sample_request
import pandas as pd


app = Flask("ts_app")
app.config["MAX_CONTENT_LENGTH"] = 7 * 1024 * 1024  # 7MB limit

glossary_data = pd.read_csv("data/glossary.csv", index_col=0).sort_index()


@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")


@app.route("/glossary")
def glossary():
    """Glossary page."""
    return render_template("glossary.html", definitions=glossary_data)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    """Process and analyse uploaded file."""
    if request.method == "POST":
        error, file_name, data = process_upload(request)

        if error:
            return render_template('upload.html', input_error=error)

        ts_results = TS(data).results
        results_df = ts_results.pop('results')
        results_df.to_csv('ts_app/static/results.csv')
        return render_template("results.html", filename=file_name,
                               **ts_results)
    return render_template("upload.html")


@app.route("/sample", methods=["GET", "POST"])
def create_sample():
    """Create and process sample time series data."""
    if request.method == "POST":
        error, data = process_sample_request(request)

        if error:
            return render_template('sample.html', input_error=error,
                                   sample_params=default_sample_params)

        ts_results = TS(data).results
        results_df = ts_results.pop('results')
        results_df.to_csv('ts_app/static/results.csv')
        return render_template("results.html", filename="Sample",
                               **ts_results)

    return render_template("sample.html",
                           sample_params=default_sample_params)


@app.route("/server_timeout")
def heroku_timeout():
    """
    Create the custom error page to be displayed if the app takes more
    than 30 seconds to process a request.
    See https://devcenter.heroku.com/articles/error-codes#h12-request-timeout
    """
    return render_template('heroku_custom_503.htm')
