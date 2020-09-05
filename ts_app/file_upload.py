
from werkzeug.utils import secure_filename
import pandas as pd
from pandas.errors import ParserError as pdParserError
from dateutil.parser import ParserError as dtParserError


def allowed_file(filename):
    """
    Check whether upload-file's extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}


def process_upload(request):
    error = None
    data = None
    filename = ''
    try:
        file = request.files["file"]
    except KeyError:
        error = "file absent"

    if file.filename == "":
        error = "file absent"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # clear_files("csv")  # remove all previous .csv uploads

        # Parse file as a pandas dataframe
        try:
            data = pd.read_csv(file, index_col=0)
            n = len(data)
            if n < 30:
                error = f"""Please try again... The uploaded file has
                    only {n} values, but the minimum is set at 30."""

            if data.shape[1] < 1:
                error = """Please ensure that the data has a date
                    column and at least one other column with numeric
                    values."""

            data = data.iloc[:, -1]  # select last column for analysis

            try:
                data = data.astype(float)
            except ValueError:
                error = """Please try again... it seems the values
                    to be processed could not be converted to numbers."""

            # Convert the index to datetime data type
            try:
                data.index = pd.to_datetime(data.index)
            except dtParserError:
                error = """Please try again... it seems that the
                    values in the 1st column could not be read as dates."""

            # If date frequency can't be inferred, some statsmodels
            # functions (e.g. seasonal_decompose) tend to break.
            if pd.infer_freq(data.index) is None:
                error = """Please try again... a uniform date
                    frequency which is needed in some of the time series
                    functions used) could not be determined."""

        except (pdParserError, UnicodeDecodeError):
            error = """Please try again... the uploaded file
                could not be parsed as a CSV file."""

    return error, filename, data
