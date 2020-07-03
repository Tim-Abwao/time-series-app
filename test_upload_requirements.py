import pytest
from app import app
import pandas as pd
import numpy as np
from io import BytesIO


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


okay_sample = pd.Series(np.random.randint(0, 100, 50),
                        index=pd.date_range('2020-01-01', periods=50))
text_like_sample = pd.Series(list('abc') * 15)
small_sample = okay_sample.iloc[:20]
sample_without_date = okay_sample.reindex(f'ID_{i}' for i in range(50))


def file_buffer(data):
    """Creates the file object to simulate uploads"""
    return BytesIO(data.to_csv().encode())


def test_file_extension(client):
    """
    Testing that posting files without the .csv extension will result in a
    redirect to the upload page.
    """
    result = client.post(
        "/upload", content_type='multipart/form-data',
        data={'file': (file_buffer(okay_sample), 'file.some_extension')},
        follow_redirects=True)
    assert b"A quick word about uploads..." in result.data
    assert result.status_code == 200


def test_valid_upload(client):
    """Testing if valid upload files are handled"""
    result = client.post(
        "/upload", content_type='multipart/form-data',
        data={'file': (file_buffer(okay_sample), 'nyef.csv')},
        follow_redirects=True)
    assert b"Graphical Output" in result.data
    assert result.status_code == 200


def test_small_size_uploads(client):
    """Testing if uploads with few values are handled"""
    result = client.post(
        "/upload", content_type='multipart/form-data',
        data={'file': (file_buffer(small_sample), 'nyef.csv')},
        follow_redirects=True)
    assert b"Please try again... The uploaded file has only 20 values"\
        in result.data
    assert result.status_code == 200


def test_non_numeric_uploads(client):
    """
    Testing if uploads with data that can't be converted to `float` type are
    handled.
    """
    result = client.post(
        "/upload",
        content_type='multipart/form-data',
        data={'file': (file_buffer(text_like_sample), 'text_sample.csv')},
        follow_redirects=True)
    assert b"the values to be processed could not be converted to numbers." \
        in result.data
    assert result.status_code == 200


def test_false_csv_uploads(client):
    """
    Testing if uploads of a non-csv format but with the .csv file extension
    are handled.
    """
    with open('static/ts.png', 'rb') as non_csv_file:
        result = client.post(
            "/upload", content_type='multipart/form-data',
            data={'file': (non_csv_file, 'png_named_as.csv')},
            follow_redirects=True)
        assert b"the uploaded file is not in standard CSV format." \
            in result.data
        assert result.status_code == 200


def test_uploads_without_dates(client):
    """
    Testing if uploads for which the first column can't be parsed as dates
    are handled.
    """
    result = client.post(
            "/upload", content_type='multipart/form-data',
            data={'file': (file_buffer(sample_without_date), 'no_dates.csv')},
            follow_redirects=True)
    assert b"the values in the 1st column could not be read as dates." \
        in result.data
    assert result.status_code == 200
