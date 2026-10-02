import os
import uuid

os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient

from app.main import app
from app.database import init_db

init_db()

client = TestClient(app)


def unique_email():
    return f"test-{uuid.uuid4().hex[:10]}@example.com"


def register_and_login():
    email = unique_email()

    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    return email


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_and_home():
    email = register_and_login()

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/generate-home",
        json={
            "budget": 50000,
            "style": "modern",
            "rooms": [
                "Living Room",
                "Bedroom",
            ],
            "notes": "simple",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["planner"] == "home"
    assert body["history_id"] is not None
    assert body["total_estimated"] <= 50000


def test_party():
    email = register_and_login()

    client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    response = client.post(
        "/generate-party",
        json={
            "budget": 30000,
            "guests": 30,
            "event_type": "birthday",
            "city": "Coimbatore",
        },
    )

    assert response.status_code == 200
    assert response.json()["planner"] == "party"


def test_jewelry():
    email = register_and_login()

    client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    response = client.post(
        "/generate-jewelry",
        data={
            "budget": "15000",
            "occasion": "wedding",
            "style": "elegant",
            "notes": "gold tone",
        },
    )

    assert response.status_code == 200
    assert response.json()["planner"] == "jewelry"


def test_history():
    email = register_and_login()

    client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    client.post(
        "/generate-home",
        json={
            "budget": 10000,
            "style": "minimal",
            "rooms": ["Bedroom"],
        },
    )

    response = client.get("/api/history")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_invalid_budget():
    email = register_and_login()

    client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    response = client.post(
        "/generate-home",
        json={
            "budget": 0,
            "style": "modern",
            "rooms": ["Bedroom"],
        },
    )

    assert response.status_code == 422


def test_logout():
    email = register_and_login()

    client.post(
        "/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    response = client.get("/logout")

    assert response.status_code == 200

    response = client.get("/session-info")

    assert response.status_code == 401
