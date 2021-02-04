from ts_app.file_upload import process_upload
import pandas as pd


good_sample = pd.DataFrame(
    range(50), index=pd.date_range('2020-01-01', periods=50))
non_numeric_sample = pd.DataFrame(list('abc') * 15)
small_sample = pd.DataFrame(range(20))
non_dated_sample = pd.DataFrame(range(50), index=[f'a{i}' for i in range(50)])


def test_file_extension():
    """
    Check if posting files without the .csv extension is handled.
    """
    error = process_upload(good_sample, 'somefile')
    assert "Please try again... invalid file name" in error


def test_valid_upload():
    """Check if valid upload files are processed."""
    error = process_upload(good_sample, 'somefile.csv')
    assert error is None


def test_small_size_uploads():
    """Check if uploads with less values than required are handled."""
    error = process_upload(small_sample, 'somefile.csv')
    assert "but the minimum is set at 30" in error


def test_non_numeric_uploads():
    """
    Check if uploads with data that can't be converted to numeric `float` type
    are handled.
    """
    error = process_upload(non_numeric_sample, 'non_numeric.csv')
    assert "could not be read as numbers." in error


def test_uploads_without_dates():
    """
    Check if uploads for which the first column can't be parsed as dates
    are handled.
    """
    error = process_upload(non_dated_sample, 'no_dates.csv')
    assert "could not be read as dates." in error
