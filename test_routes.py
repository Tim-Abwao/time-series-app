import pytest
from app import app
from datetime import date, timedelta

_start_date = date.today().isoformat()
_end_date = (date.today() + timedelta(days=30)).isoformat()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """Testing the index page"""

    rv = client.get("/")
    assert b"A simple app to learn about, and apply" in rv.data


def test_sampling_page(client):
    """Testing the sample creation page"""

    rv = client.get("/sample")
    assert b"The sample is created using a random number generator" in rv.data


def test_upload_page(client):
    """Testing the file upload page"""

    rv = client.get("/upload")
    assert b"A quick word about uploads..." in rv.data


def test_post_no_file(client):
    """Testing the result of not uploading acceptable file"""

    rv = client.post("/upload", data={'filename': 'file.csv'})
    assert b"A quick word about uploads..." in rv.data


def test_glossary_page(client):
    """Testing the glossary page"""

    rv = client.get("/glossary")
    assert b"Glossary of Time Series Terms" in rv.data


def test_sample_creation(client):
    """Testing the sample creation page"""

    rv = client.post(
        "/sample",
        data=dict(
            start_date=_start_date,
            end_date=_end_date,
            frequency="D",
            ar_order=1,
            ma_order=1,
        ),
        follow_redirects=True
    )
    assert b"Graphical Output" in rv.data


def test_small_sample_creation(client):
    """Testing if small samples are handled"""

    rv = client.post(
        "/sample",
        data=dict(
            start_date=_start_date,
            end_date=_end_date,
            frequency="M",
            ar_order=1,
            ma_order=1,
        ),
        follow_redirects=True
    )
    assert b"Please try again... Generated sample too small." in rv.data
