from httpx import AsyncClient


async def test_read_users_me(auth_async_client: AsyncClient):
    response = await auth_async_client.get("/users/me")
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == "user@example.com"
