import os
import sys
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.json.get("status") == "healthy"

if __name__ == "__main__":
    os.system("pip install pytest")
    os.system("pytest -q")