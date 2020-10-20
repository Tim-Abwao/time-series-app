from datetime import date, timedelta
import pytest
import ts_app as app


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client


sample_params = {
    'start_date': date.today().isoformat(),
    'end_date': (date.today() + timedelta(days=30)).isoformat(),
    'frequency': "D",
    'ar_order': 1,
    'ma_order': 1}


def test_sample_creation(client):
    """Check sample creation page."""
    result = client.post("/sample", data=sample_params, follow_redirects=True)
    assert b"Summary for Sample" in result.data
    assert result.status_code == 200


def test_small_sample_creation(client):
    """Check if small samples are handled."""
    # there's only 1 month in 30 days, resulting in a very small sample
    sample_params['frequency'] = 'M'
    result = client.post("/sample", data=sample_params, follow_redirects=True)
    assert b"but the minimum sample size is set" in result.data
    assert result.status_code == 200
    sample_params['frequency'] = 'D'  # restoring initial frequency
