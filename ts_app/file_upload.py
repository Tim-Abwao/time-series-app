import pandas as pd
from dateutil.parser import ParserError as dtParserError


def process_upload(data):
    """Validate the data from the uploaded file.

    Parameters
    ----------
    data : pandas.Dataframe
        The data extracted from the file.

    Returns
    -------
    The error found, if any, or a pandas Series with the data's last column.
    """
    # Ensure the data has more than 30 values.
    if (n := len(data)) < 30:
        return f"""Please try again... the uploaded file has only {n} values,
                   but the minimum is set at 30."""

    # Ensure the dates(index) can be converted to datetime objects having a
    # consistent frequency.
    try:
        data.index = pd.to_datetime(data.index)
        # If date frequency can't be inferred, or is not consistent, some
        # statsmodels functions tend to break.
        if pd.infer_freq(data.index) in {None, "N"}:
            return """Please try again... a uniform date frequency (which is
                      needed in some of the time series functions used) could
                      not be determined."""
    except (dtParserError, ValueError):
        return """Please try again... it seems that the values in the 1st
                  column could not be read as dates."""

    # Ensure the data has at least 2 columns.
    # Since the first column is read as the index, there has to be at least
    # one other column with values.
    # If multiple columns exist, only the last is considered.
    try:
        data = data.iloc[:, -1]  # select the last column for analysis
    except IndexError:
        return """Please ensure that the data has a date index and at least
                  one other column with numeric values."""

    # Ensure the data values are numeric
    try:
        data = data.astype("float32")
    except ValueError:
        return """Please try again... it seems the values to be processed
                  could not be read as numbers."""
