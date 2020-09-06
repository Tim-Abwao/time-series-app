import pytest
import ts_app as app


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client


def test_homepage(client):
    """Check home page."""
    result = client.get("/")
    assert b"A simple app to learn about, and apply" in result.data
    assert result.status_code == 200


def test_glossary_page(client):
    """Check glossary page."""
    result = client.get("/glossary")
    assert b"Glossary of Time Series Terms" in result.data
    assert result.status_code == 200


def test_upload_page(client):
    """Check file upload page."""
    result = client.get("/upload")
    assert b"A quick word about uploads..." in result.data
    assert result.status_code == 200


def test_sample_page(client):
    """Check sample creation page."""
    result = client.get("/sample")
    assert b"Creating a sample" in result.data
    assert result.status_code == 200


def test_custom_error_page(client):
    """Check the Heroku-timeout-error custom page."""
    result = client.get("/server_timeout")
    assert b"Oops! The server timed out" in result.data
    assert result.status_code == 200
