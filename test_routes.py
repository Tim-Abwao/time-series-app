import pytest
from app import app
from datetime import date, timedelta
import pandas as pd
import numpy as np
import os

_start_date = date.today().isoformat()
_end_date = (date.today() + timedelta(days=30)).isoformat()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """Testing the index page"""

    result = client.get("/")
    assert b"A simple app to learn about, and apply" in result.data
    assert result.status_code == 200


def test_sampling_page(client):
    """Testing the sample creation page"""

    result = client.get("/sample")
    assert b"Creating a sample" in result.data
    assert result.status_code == 200


def test_upload_page(client):
    """Testing the file upload page"""

    result = client.get("/upload")
    assert b"A quick word about uploads..." in result.data
    assert result.status_code == 200


def test_file_processing(client):
    """Testing the upload-file processing page."""

    # creating a sample file where uploads are saved
    pd.DataFrame(
        np.random.randint(100, 500, 50),
        index=pd.date_range("2020-01-01", periods=50, freq="D"),
    ).to_csv("static/files/sample.csv")
    # processing the sample as an uploaded file would've been
    result = client.post("/processing_sample.csv", data={"filename": "sample.csv"})
    os.remove("static/files/sample.csv")
    assert b"Results for sample.csv" in result.data
    assert result.status_code == 200


def test_glossary_page(client):
    """Testing the glossary page"""

    result = client.get("/glossary")
    assert b"Glossary of Time Series Terms" in result.data
    assert result.status_code == 200


def test_sample_creation(client):
    """Testing the sample creation page"""

    result = client.post(
        "/sample",
        data=dict(
            start_date=_start_date,
            end_date=_end_date,
            frequency="D",
            ar_order=1,
            ma_order=1,
        ),
        follow_redirects=True,
    )
    assert b"Results for Sample" in result.data
    assert result.status_code == 200


def test_small_sample_creation(client):
    """Testing if small samples are handled"""

    result = client.post(
        "/sample",
        data=dict(
            start_date=_start_date,
            end_date=_end_date,
            frequency="M",
            ar_order=1,
            ma_order=1,
        ),
        follow_redirects=True,
    )
    assert b"Please try again... Generated sample too small." in result.data
    assert result.status_code == 200
