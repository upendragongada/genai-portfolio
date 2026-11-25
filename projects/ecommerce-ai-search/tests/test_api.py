
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

import api
from fastapi.testclient import TestClient

client = TestClient(api.app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_search_endpoint(monkeypatch):
    fake_hits = [
        {
            "_score": 0.95,
            "_source": {
                "id": 1,
                "name": "Apple iPhone 16",
                "category": "Smartphones",
                "price": 69999
            }
        }
    ]

    monkeypatch.setattr(api, "hybrid_search", lambda q, top_k: fake_hits)

    response = client.get(
        "/search",
        params={"q": "smartphone", "top_k": 5}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "smartphone"
    assert data["count"] == 1
    assert data["results"][0]["name"] == "Apple iPhone 16"


def test_search_rejects_short_query():
    response = client.get("/search", params={"q": "a"})

    assert response.status_code == 422
