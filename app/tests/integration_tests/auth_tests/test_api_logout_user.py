from httpx import AsyncClient


async def test_api_logout_user(auth_async_client: AsyncClient):
    await auth_async_client.post("/auth/logout")
    assert not auth_async_client.cookies.get("booking_access_token")
