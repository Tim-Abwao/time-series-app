import pytest
from app import app
import pandas as pd
import numpy as np
from io import StringIO, BytesIO


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


okay_sample = pd.Series(np.random.randint(0, 100, 50),
                        index=pd.date_range('2020-01-01', periods=50))
small_sample = okay_sample.iloc[:20]


def file_buffer(data_frame):
    buffer = StringIO()
    data_frame.to_csv(buffer)  # df.to_csv can't yet write to binary objects
    buffer.seek(0)
    return BytesIO(buffer.getvalue().encode())


def test_file_upload(client):
    """Testing if valid upload files are handled"""
    result = client.post(
        "/upload", content_type='multipart/form-data',
        data={'file': (file_buffer(okay_sample), 'nyef.csv')},
        follow_redirects=True)
    assert b"Graphical Output" in result.data
    assert result.status_code == 200


def test_small_upload_size(client):
    """Testing if uploads with few values are handled"""
    result = client.post(
        "/upload", content_type='multipart/form-data',
        data={'file': (file_buffer(small_sample), 'nyef.csv')},
        follow_redirects=True)
    assert b"Please try again... The uploaded file has only 20 values"\
        in result.data
    assert result.status_code == 200
