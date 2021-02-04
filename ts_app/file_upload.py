import pandas as pd
from dateutil.parser import ParserError as dtParserError
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """Check whether the uploaded file's extension is allowed.

    Parameters:
    ----------
    filename: str
    """
    okay_file = {'csv', 'xls', 'xlsx'}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in okay_file


def process_upload(data, file_name):
    """Get the data from the file uploaded in the given request.

    Parameters:
    ----------
    request: flask.Request
        A Flask request object with data from the file-upload-form.

    Returns:
    -------
    The error, if present, or None if the upload is successful.
    """
    if allowed_file(file_name):
        # Clean the file_name
        file_name = secure_filename(file_name)
    else:
        return "Please try again... invalid file name."

    if (n := len(data)) < 30:
        return f"""Please try again... the uploaded file has only {n} values,
                   but the minimum is set at 30."""

    try:
        data = data.iloc[:, -1]  # select the last column for analysis
    except IndexError:
        return """Please ensure that the data has a date index and at least
                  one other column with numeric values."""

    try:
        data = data.astype('float32')
    except ValueError:
        return """Please try again... it seems the values to be processed
                  could not be read as numbers."""

    try:
        data.index = pd.to_datetime(data.index)
        # If date frequency can't be inferred, or is not consistent, some
        # statsmodels functions tend to break.
        if pd.infer_freq(data.index) is None:
            return """Please try again... a uniform date frequency (which is
                      needed in some of the time series functions used) could
                      not be determined."""
    except (dtParserError, ValueError):
        return """Please try again... it seems that the values in the 1st
                  column could not be read as dates."""

    # Persist data if all check pass
    data.rename(file_name).to_pickle('ts-app-data.temp')
