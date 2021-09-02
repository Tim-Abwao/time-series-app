from typing import Optional

import pandas as pd
from dateutil.parser import ParserError as dtParserError


def process_upload(data: pd.DataFrame) -> Optional[str]:
    """Validate the data from the uploaded file.

    Parameters
    ----------
    data : pandas.DataFrame
        The data extracted from the file.

    Returns
    -------
    Optional[str]
        The error found, if any.
    """
    if (n := len(data)) < 32:
        return (
            f"Please try again... the uploaded file has only {n} values, but"
            " the minimum is set at 32."
        )

    # Ensure the dates(index) can be converted to datetime objects having a
    # consistent frequency.
    # If date frequency can't be inferred, or is not consistent, some
    # statsmodels time series functions won't work.
    try:
        data.index = pd.to_datetime(data.index)

        if pd.infer_freq(data.index) in {None, "N"}:
            return (
                "Please try again... a uniform date frequency "
                "(which is needed in some of the time series functions used) "
                "could not be determined."
            )
    except (dtParserError, ValueError):
        return (
            "Please try again... it seems that the values in the 1st column "
            "could not be read as dates."
        )

    # Ensure the data has at least 2 columns, since the first column is read
    # as the index.
    # If multiple columns exist, consider the right-most (last).
    try:
        data = data.select_dtypes(include="number").iloc[:, -1]
    except IndexError:
        return (
            "Please ensure that the data has a date index and at least one "
            "other column with numeric values."
        )
