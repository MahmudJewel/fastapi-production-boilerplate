from uuid import uuid4

import pytest

from app.models.user_model import User


@pytest.mark.asyncio
async def test_create_user_creates_db_object(client, db_session):
    email = f"integration_user_{uuid4().hex[:8]}@mail.com"
    payload = {
        "email": email,
        "password": "MyStrongPass123!",
        "first_name": "Mahmud",
        "last_name": "Jewel",
    }

    response = await client.post("/users/", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == payload["email"]
    assert isinstance(body["id"], str)
    assert body["id"]

    inserted_user = db_session.query(User).filter(User.email == payload["email"]).first()
    assert inserted_user is not None
    assert inserted_user.first_name == payload["first_name"]
    assert inserted_user.last_name == payload["last_name"]


@pytest.mark.asyncio
async def test_duplicate_email_returns_400_and_single_row(client, db_session):
    email = f"integration_dup_{uuid4().hex[:8]}@mail.com"
    payload = {
        "email": email,
        "password": "MyStrongPass123!",
        "first_name": "Mahmud",
        "last_name": "Jewel",
    }

    first_response = await client.post("/users/", json=payload)
    second_response = await client.post("/users/", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "User already exists"}

    row_count = db_session.query(User).filter(User.email == payload["email"]).count()
    assert row_count == 1
