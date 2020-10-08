from werkzeug.utils import secure_filename
import pandas as pd
from dateutil.parser import ParserError as dtParserError


def allowed_file(filename):
    """
    Check whether the uploaded file's extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}


def process_upload(request):
    """Get the data from the file uploaded in the given request."""
    try:
        file = request.files["file"]
        error = None
    except KeyError:
        file = ""

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    else:
        filename = ""
        error = "Please try again... no file has been received."
        data = []
        return error, filename, data

    # Parse valid upload as a pandas DataFrame
    try:
        data = pd.read_csv(file, index_col=0)

        if (n := len(data)) < 30:
            error = f"""Please try again... The uploaded file has only {n}
                     values, but the minimum is set at 30."""

        try:
            data = data.iloc[:, -1]  # select last column for analysis
        except IndexError:
            error = """Please ensure that the data has a date column and at
                       least one other column with numeric values."""

        try:
            data = data.astype(float)
        except ValueError:
            error = """Please try again... it seems the values to be processed
                       could not be converted to numbers."""

        # Convert the index to datetime data type
        try:
            data.index = pd.to_datetime(data.index)

            # If date frequency can't be inferred, some statsmodels
            # functions (e.g. seasonal_decompose) tend to break.
            if pd.infer_freq(data.index) is None:
                error = """Please try again... a uniform date frequency which
                           is needed in some of the time series functions used)
                           could not be determined."""
        except (dtParserError, TypeError):
            error = """Please try again... it seems that the values in the 1st
                       column could not be read as dates."""

    except (pd.errors.ParserError, UnicodeDecodeError):
        error = """Please try again... the uploaded file could not be parsed
                   as CSV."""

    return error, filename, data
