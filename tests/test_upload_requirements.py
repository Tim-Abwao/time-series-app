import numpy as np
import pandas as pd
import pytest
from io import BytesIO
from ts_app import server


@pytest.fixture
def client():
    server.config["TESTING"] = True
    with server.test_client() as client:
        yield client


good_sample = pd.Series(np.random.randint(0, 100, 50),
                        index=pd.date_range('2020-01-01', periods=50))
non_numeric_sample = pd.Series(list('abc') * 15)
small_sample = good_sample.iloc[:20]
non_dated_sample = good_sample.reindex(f'ID_{i}' for i in range(50))


def file_buffer(data):
    """Creates the file object to simulate uploads"""
    return BytesIO(data.to_csv().encode())


def test_file_extension(client):
    """
    Check if posting files without the .csv extension causes a redirect to the
    upload page.
    """
    result = client.post("/upload", content_type='multipart/form-data',
                         data={'file': (file_buffer(good_sample),
                                        'file.some_extension')},
                         follow_redirects=True)
    assert b"Please try again... no CSV file detected" in result.data
    assert result.status_code == 200


def test_valid_upload(client):
    """Check if valid upload files are processed."""
    result = client.post("/upload", content_type='multipart/form-data',
                         data={'file': (file_buffer(good_sample),
                                        'data.csv')},
                         follow_redirects=True)
    assert b"Loading..." in result.data
    assert result.status_code == 200


def test_small_size_uploads(client):
    """Check if uploads with less values than required are handled."""
    result = client.post("/upload", content_type='multipart/form-data',
                         data={'file': (file_buffer(small_sample),
                                        'data.csv')},
                         follow_redirects=True)
    assert b"but the minimum is set at 30" in result.data
    assert result.status_code == 200


def test_non_numeric_uploads(client):
    """
    Check if uploads with data that can't be converted to numeric `float` type
    are handled.
    """
    result = client.post("/upload", content_type='multipart/form-data',
                         data={'file': (file_buffer(non_numeric_sample),
                                        'non_numeric.csv')},
                         follow_redirects=True)
    assert b"could not be read as numbers." in result.data
    assert result.status_code == 200


def test_uploads_without_dates(client):
    """
    Check if uploads for which the first column can't be parsed as dates
    are handled.
    """
    result = client.post("/upload", content_type='multipart/form-data',
                         data={'file': (file_buffer(non_dated_sample),
                                        'no_dates.csv')},
                         follow_redirects=True)
    assert b"could not be read as dates." in result.data
    assert result.status_code == 200
