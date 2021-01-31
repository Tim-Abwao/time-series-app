import pytest
from ts_app import server


@pytest.fixture
def client():
    server.config["TESTING"] = True
    with server.test_client() as client:
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
