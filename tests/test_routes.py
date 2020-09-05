import pytest
from ts_app.app import app
from datetime import date, timedelta
import pandas as pd
import numpy as np
import os

sample_params = {
    'start_date': date.today().isoformat(),
    'end_date': (date.today() + timedelta(days=30)).isoformat(),
    'frequency': "D",
    'ar_order': 1,
    'ma_order': 1}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """Check home page."""
    result = client.get("/")
    assert b"A simple app to learn about, and apply" in result.data
    assert result.status_code == 200


def test_sampling_page(client):
    """Check sample creation page."""
    result = client.get("/sample")
    assert b"Creating a sample" in result.data
    assert result.status_code == 200


def test_upload_page(client):
    """Check file upload page."""
    result = client.get("/upload")
    assert b"A quick word about uploads..." in result.data
    assert result.status_code == 200


def test_file_processing(client):
    """Check upload file processing page."""
    # creating a sample file where uploads are saved
    pd.DataFrame(
        np.random.randint(100, 500, 50),
        index=pd.date_range("2020-01-01", periods=50, freq="D"),
    ).to_csv("static/files/sample.csv")
    # processing the sample as an uploaded file would've been
    result = client.post("/processing_sample.csv",
                         data={"filename": "sample.csv"})
    os.remove("static/files/sample.csv")
    assert b"Results for sample.csv" in result.data
    assert result.status_code == 200


def test_glossary_page(client):
    """Check glossary page."""
    result = client.get("/glossary")
    assert b"Glossary of Time Series Terms" in result.data
    assert result.status_code == 200


def test_sample_creation(client):
    """Check sample creation page."""
    result = client.post("/sample", data=sample_params, follow_redirects=True)
    assert b"Results for Sample" in result.data
    assert result.status_code == 200


def test_small_sample_creation(client):
    """Check if small samples are handled."""
    # there's only 1 month in 30 days, resulting in a very small sample
    sample_params['frequency'] = 'M'
    result = client.post("/sample", data=sample_params, follow_redirects=True)
    assert b"but the minimum sample size is set" in result.data
    assert result.status_code == 200
    sample_params['frequency'] = 'D'  # restoring initial frequency


def test_custom_error_page(client):
    """Check the Heroku-timeout-error custom page."""
    result = client.get("/server_timeout")
    assert b"Oops! The server timed out" in result.data
    assert result.status_code == 200
