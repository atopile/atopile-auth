import os
import httpx
import pytest
from fastapi.testclient import TestClient
import supabase


@pytest.fixture
def test_client():
    from fastapi import Security, FastAPI
    from atopile_auth.supabase_bearer import SupabaseBearer

    app = FastAPI()
    client = supabase.create_client(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
    )

    bearer = SupabaseBearer(client)

    @app.get("/")
    async def root(
        claims=Security(bearer),
    ):
        return claims.get("claims")

    return TestClient(app)


def test_invalid_auth(test_client: TestClient):
    response = test_client.get("/", headers={"Authorization": "Bearer invalid-token"})
    with pytest.raises(httpx.HTTPStatusError) as e:
        response.raise_for_status()

    assert e.value.response.status_code == 403


def test_no_auth(test_client: TestClient):
    response = test_client.get("/")
    with pytest.raises(httpx.HTTPStatusError) as e:
        response.raise_for_status()

    assert e.value.response.status_code == 403


def test_with_auth(test_client: TestClient):
    client = supabase.create_client(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
    )
    client.auth.sign_in_with_password(
        {
            "email": os.getenv("TEST_EMAIL"),
            "password": os.getenv("TEST_PASSWORD"),
        }
    )

    response = test_client.get(
        "/",
        headers={"Authorization": f"Bearer {client.auth.get_session().access_token}"},
    )
    response.raise_for_status()

    assert response.status_code == 200
