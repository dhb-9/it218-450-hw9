# pylint: disable=missing-module-docstring, missing-function-docstring
import pytest
from httpx import AsyncClient
from app.main import app  # Adjust import path as necessary

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
async def get_access_token_for_test(test_client):
    form_data = {"username": "admin", "password": "secret"}
    response = await test_client.post("/token", data=form_data)
    return response.json()["access_token"]
