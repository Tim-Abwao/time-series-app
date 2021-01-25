from werkzeug.utils import secure_filename
import pandas as pd
from dateutil.parser import ParserError as dtParserError


def allowed_file(filename):
    """
    Check whether the uploaded file's extension is allowed.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"csv"}


def process_upload(request):
    """Get the data from the file uploaded in the given request.

    Parameters:
    ----------
    request: flask.Request
        A Flask request object with data from the file-upload-form.

    Returns:
    -------
    A tuple, (error, filename, data).
    """
    try:
        file = request.files["file"]  # get file in request data
        error = None
    except KeyError:
        file = ""

    if file and allowed_file(file.filename):
        # if a file is present, and it has the '.csv' extension
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
            return error, filename, data

        try:
            data = data.iloc[:, -1]  # select last column for analysis
        except IndexError:
            error = """Please ensure that the data has a date column and at
                       least one other column with numeric values."""

        try:
            data = data.astype('float32')
        except ValueError:
            error = """Please try again... it seems the values to be processed
                       could not be read as numbers."""

        # Convert the index to a datetime index
        try:
            data.index = pd.to_datetime(data.index)

            # If date frequency can't be inferred, some statsmodels
            # functions (e.g. seasonal_decompose) tend to break.
            if pd.infer_freq(data.index) is None:
                error = """Please try again... a uniform date frequency (which
                           is needed in some of the time series functions used)
                           could not be determined."""
        except (dtParserError, TypeError):
            error = """Please try again... it seems that the values in the 1st
                       column could not be read as dates."""

    except (pd.errors.ParserError, UnicodeDecodeError):
        # If the csv file can't be parsed as a pandas dataframe
        error = """Please try again... the uploaded file could not be parsed
                   as CSV."""
        data = None

    return error, filename, data
