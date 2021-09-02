import pandas as pd
from ts_app.file_upload import process_upload

date_index = pd.date_range("2020-01-01", periods=50)

good_sample = pd.DataFrame(range(50), index=date_index)
non_numeric_sample = pd.DataFrame(list("abcde") * 10, index=date_index)
small_sample = pd.DataFrame(range(20), index=date_index[:20])
non_dated_sample = pd.DataFrame(range(50), index=[f"a{i}" for i in range(50)])


def test_valid_upload():
    error = process_upload(good_sample)
    assert error is None


def test_small_size_uploads():
    error = process_upload(small_sample)
    assert "but the minimum is set at 32" in error


def test_non_numeric_uploads():
    error = process_upload(non_numeric_sample)
    assert "at least one other column with numeric values" in error


def test_uploads_without_dates():
    error = process_upload(non_dated_sample)
    assert "could not be read as dates." in error
