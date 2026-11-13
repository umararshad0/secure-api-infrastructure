import os
from dotenv import load_dotenv

load_dotenv()
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app, base_url="http://localhost")
rate_limit_client = TestClient(
    app,
    base_url="http://localhost",
    client=("198.51.100.10", 12345)
)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to Secure API Infrastructure",
        "status": "running"
    }
def test_items_without_api_key():
    response = client.get("/items")

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or missing API key"
    }
def test_items_with_invalid_api_key():
    response = client.get(
        "/items",
        headers={"X-API-Key": "wrong-api-key"}
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or missing API key"
    }
def test_items_with_valid_api_key():
    api_key = os.getenv("API_KEY")

    assert api_key is not None

    response = client.get(
        "/items",
        headers={"X-API-Key": api_key}
    )

    assert response.status_code == 200
def test_pagination():
    api_key = os.getenv("API_KEY")

    response = client.get(
        "/items?page=1&limit=2",
        headers={"X-API-Key": api_key}
    )

    assert response.status_code == 200

    assert response.json() == {
        "items": [
            {"id": 1, "name": "Server"},
            {"id": 2, "name": "Database"}
        ]
    }
def test_invalid_pagination():
    api_key = os.getenv("API_KEY")

    response = client.get(
        "/items?page=0",
        headers={"X-API-Key": api_key}
    )

    assert response.status_code == 422
def test_invalid_item_validation():
    api_key = os.getenv("API_KEY")

    response = client.post(
        "/items",
        headers={"X-API-Key": api_key},
        json={
            "id": "hello",
            "name": ""
        }
    )

    assert response.status_code == 422
def test_rate_limit():
    api_key = os.getenv("API_KEY")

    responses = []

    for _ in range(6):
        response = rate_limit_client.get(
            "/items",
            headers={"X-API-Key": api_key}
        )
        responses.append(response.status_code)

    assert responses == [200, 200, 200, 200, 200, 429]
def test_create_item():
    api_key = os.getenv("API_KEY")

    response = client.post(
        "/items",
        headers={"X-API-Key": api_key},
        json={
            "id": 10,
            "name": "Cloud Server"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": 10,
        "name": "Cloud Server"
    }