from flask import Flask, render_template, url_for, request, redirect
from ts_functions import TimeSeriesPredictions, TimeSeriesGraphs
from ts_functions import clear_old_files
from werkzeug.utils import secure_filename
from datetime import date, timedelta
import pandas as pd
from pandas.errors import EmptyDataError, ParserError as pdParserError
from dateutil.parser import ParserError as dtParserError
import numpy as np
from statsmodels.tsa.arima_process import arma_generate_sample


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

glossary_data = pd.read_csv("static/glossary.csv").sort_values(by="title")
glossary_data.reset_index(drop=True, inplace=True)

frequencies = {
    "D": "Days",
    "B": "Business days",
    "w": "Weeks",
    "M": "Months",
    "Q": "Quarters",
    "Y": "Years",
}


def allowed_file(filename):
    """
    Checks whether a file's extension is supported/allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}


def get_ts_results(data):
    """
    A convenience funtion to nicely consolidate the output/results
    """
    time_series_results = {}
    # fitting the time series models
    predictions = TimeSeriesPredictions(data)
    time_series_results['results'] = results = predictions.results
    time_series_results['sample'] = sample = predictions.sample
    time_series_results['totals'] = sample.sum().round(2).to_numpy()
    results.to_csv('static/results.csv')
    # removing old graphs
    clear_old_files("png")
    # plotting the current results
    plots = TimeSeriesGraphs(data, results)
    time_series_results['graphs'] = {
        "acf&pacf": plots.acf_pacf,
        "lineplot": plots.lineplot,
        "model_fit": plots.modelfit,
        "seasonal_decomposition": plots.seasonal_decomposition
    }
    return time_series_results


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/glossary")
def glossary():
    return render_template("glossary.html", definitions=glossary_data)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # selecting the file part
        try:
            file = request.files["file"]
        except KeyError:
            return redirect(request.url)

        # Ensuring the file exists (some browsers send an empty file part if
        # no file is selected).
        if file.filename == "":
            return redirect(request.url)

        # processing the file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            clear_old_files("csv")  # removing outdated uploads
            try:
                data = pd.read_csv(file, index_col=0)
            except (pdParserError, UnicodeDecodeError):
                # raised if the file isn't CSV
                input_error = "Please try again... the uploaded file is not" +\
                    " in standard CSV format."
                return render_template("upload.html", input_error=input_error)

            try:
                data.index = pd.to_datetime(data.index)
            except (dtParserError, TypeError):
                # raised if index can't be read as dates
                input_error = "Please try again... it seems that the values" +\
                    " in the 1st column could not be read as dates."
                return render_template("upload.html", input_error=input_error)

            if len(data) < 30:  # avoiding errors due to small samples
                # String concatenation is used to minimize the tab characters
                # (indentation) that appear in the generated html text.
                input_error = "Please try again... The uploaded file has " +\
                 f"only {len(data)} values, but the minimum is set at 30."
                return render_template("upload.html", input_error=input_error)

            # Handling cases where date frequency can't be inferred, which
            # breaks some statsmodels functions (e.g. seasonal_decompose)
            if pd.infer_freq(data.index) is None:
                input_error = "Please try again... a uniform date frequency" +\
                 "(which is needed in some of the time series functions used)"\
                 + "could not be determined."
                return render_template("upload.html", input_error=input_error)

            if data.shape[1] < 1:
                input_error = "Please ensure that the data has a date column\
                              and at least one other column."
                return render_template("upload.html", input_error=input_error)

            # saving the file, if it is valid
            data = data.iloc[:, -1]  # selecting last column for analysis

            try:
                data = data.astype('float32')
            except ValueError:
                input_error = "Please try again... it seems the values to be"\
                   + " processed could not be converted to numbers."
                return render_template("upload.html", input_error=input_error)
            data.to_csv("static/files/" + filename)
            return redirect(url_for("process_file", filename=filename))

    return render_template("upload.html")


@app.route("/processing_<filename>", methods=["GET", "POST"])
def process_file(filename):
    # importing data from uploaded file
    try:
        data = pd.read_csv("static/files/" + filename, index_col=0)
        data = data.iloc[:, -1]  # selecting last column for analysis
        data.index = pd.to_datetime(data.index)
    except (EmptyDataError, FileNotFoundError):  # raised if file wasn't saved
        input_error = "Please try uploading the file again."
        return render_template("upload.html", input_error=input_error)

    return render_template(
        "processing_file.html",
        filename=filename,
        **get_ts_results(data)
    )


@app.route("/sample", methods=["GET", "POST"])
def create_sample():
    today = date.today().isoformat()
    month_later = (date.today() + timedelta(days=30)).isoformat()
    if request.method == "POST":
        try:
            # collecting parameters from form
            start = request.form["start_date"]
            stop = request.form["end_date"]
            frequency = request.form["frequency"]
            ar_order = int(request.form["ar_order"])
            ma_order = int(request.form["ma_order"])
        except KeyError:
            start, stop = today, month_later
            frequency, ar_order, ma_order = "D", 1, 1

        index = pd.date_range(start, stop, freq=frequency)
        size = len(index)

        # Limit sample size to >= 30
        if size < 30:
            input_error = f"""
            Please try again... The generated sample has {size} value(s)
            ({frequencies[frequency]}) between {start} and {stop}, but
            the minimum sample size is set at 30."""
            return render_template(
                "processing_sample.html",
                frequencies=frequencies,
                today=today,
                month_later=month_later,
                input_error=input_error,
            )

        # creating user-defined ARMA sample
        np.random.seed(123)
        ar = np.linspace(-0.9, 0.9, ar_order)
        ma = np.linspace(-1, 1, ma_order)
        arma_sample = arma_generate_sample(
            ar, ma, size, scale=100, distrvs=np.random.standard_normal
        )
        data = pd.Series(arma_sample, index=index, name="Sample")

        return render_template(
            "processing_file.html",
            filename="Sample",
            **get_ts_results(data)
        )

        return render_template(
            "processing_sample.html",
            frequencies=frequencies,
            today=today,
            month_later=month_later,
            input_error=input_error,
        )

    return render_template(
        "processing_sample.html",
        sample=True,
        frequencies=frequencies,
        today=today,
        month_later=month_later,
    )


if __name__ == "__main__":
    app.run()
