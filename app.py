from flask import Flask, render_template, url_for, request, redirect
from fit_time_series import TimeSeriesResults, clear_files
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


def allowed_file(filename):
    """
    Check whether upload-file's extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}


def get_ts_results(data):
    """
    Parse results as a dict to pass to display in the html templates.
    """
    clear_files('svg')

    result = TimeSeriesResults(data)
    ts_results = {
        'results': result.predictions,
        'sample': result.predictions.tail(14),
        'graphs': {
            "acf&pacf": result.acf_pacf,
            "lineplot": result.lineplot,
            "model_fit": result.modelfit,
            "seasonal_decomposition": result.seasonal_decomposition
        }
    }
    ts_results['totals'] = ts_results['sample'].sum().to_numpy(),
    ts_results['results'].to_csv('static/results.csv')
    return ts_results


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
    """Process and save uploaded file."""
    if request.method == "POST":
        try:
            file = request.files["file"]
        except KeyError:
            return redirect(request.url)

        if file.filename == "":  # if file not suplied to input form
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            clear_files("csv")  # remove all previous .csv uploads

            # Parse file as a pandas dataframe
            try:
                data = pd.read_csv(file, index_col=0)
                if (n := len(data)) < 30:
                    input_error = f"""Please try again... The uploaded file has
                        only {n} values, but the minimum is set at 30."""
                    return render_template("upload.html",
                                           input_error=input_error)
                if data.shape[1] < 1:
                    input_error = """Please ensure that the data has a date
                        column and at least one other column with numeric
                        values."""
                    return render_template("upload.html",
                                           input_error=input_error)
                data = data.iloc[:, -1]  # select last column for analysis

                try:
                    data = data.astype(float)
                except ValueError:
                    input_error = """Please try again... it seems the values
                        to be processed could not be converted to numbers."""
                    return render_template("upload.html",
                                           input_error=input_error)
                # Convert the index to datetime data type
                try:
                    data.index = pd.to_datetime(data.index)
                except dtParserError:
                    input_error = """Please try again... it seems that the
                        values in the 1st column could not be read as dates."""
                    return render_template("upload.html",
                                           input_error=input_error)

                # If date frequency can't be inferred, some statsmodels
                # functions (e.g. seasonal_decompose) tend to break.
                if pd.infer_freq(data.index) is None:
                    input_error = """Please try again... a uniform date
                        frequency which is needed in some of the time series
                        functions used) could not be determined."""
                    return render_template("upload.html",
                                           input_error=input_error)

                data.to_csv("static/files/" + filename)

            except pdParserError:
                input_error = """Please try again... the uploaded file could
                    not be parsed as a CSV file."""
                return render_template("upload.html", input_error=input_error)

            return redirect(url_for("process_file", filename=filename))

    return render_template("upload.html")


@app.route("/processing_<filename>", methods=["GET", "POST"])
def process_file(filename):
    """
    Analyse uploaded data, and transmit results to html template.
    """
    try:
        data = pd.read_csv("static/files/" + filename, index_col=0)
        data.index = pd.to_datetime(data.index)
    except (EmptyDataError, FileNotFoundError):
        input_error = "Please try uploading the file once again."
        return render_template("upload.html", input_error=input_error)
    return render_template("processing_file.html", filename=filename,
                           **get_ts_results(data))


@app.route("/sample", methods=["GET", "POST"])
def create_sample():
    """Create and process sample time series data."""
    sample_params = {'start': date.today().isoformat(),
                     'end': (date.today() + timedelta(days=30)).isoformat(),
                     'frequencies': {"D": "Days",
                                     "B": "Business days",
                                     "w": "Weeks",
                                     "M": "Months",
                                     "Q": "Quarters",
                                     "Y": "Years",
                                     }
                     }

    if request.method == "POST":
        try:
            start = request.form["start_date"]
            stop = request.form["end_date"]
            frequency = request.form["frequency"]
            ar_order = int(request.form["ar_order"])
            ma_order = int(request.form["ma_order"])
        except KeyError:
            start, stop = sample_params['start'], sample_params['end']
            frequency, ar_order, ma_order = "D", 1, 1

        index = pd.date_range(start, stop, freq=frequency)
        if n := len(index) < 30:
            input_error = f"""Please try again... The generated sample has
                {n} value(s) ({sample_params['frequencies'][frequency]})
                between {start} and {stop}, but the minimum sample size is set
                at 30."""
            return render_template("processing_sample.html",
                                   sample_params=sample_params,
                                   input_error=input_error)

        np.random.seed(123)
        ar = np.linspace(-0.9, 0.9, ar_order)
        ma = np.linspace(-1, 1, ma_order)
        arma_sample = arma_generate_sample(
            ar, ma, len(index), scale=100, distrvs=np.random.standard_normal
        )
        data = pd.Series(arma_sample, index=index, name="Sample")

        return render_template("processing_file.html", filename="Sample",
                               **get_ts_results(data))

    return render_template("processing_sample.html",
                           sample_params=sample_params)


@app.route("/server_timeout")
def heroku_timeout():
    """
    Create the custom error page to be displayed if the app takes more
    than 30 seconds to process a request.
    See https://devcenter.heroku.com/articles/error-codes#h12-request-timeout
    """
    return render_template('heroku_custom_503.htm')


if __name__ == "__main__":
    app.run()
