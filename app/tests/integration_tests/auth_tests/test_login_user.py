from httpx import AsyncClient
from pytest import mark


@mark.parametrize("email, password, status_code", [
    # Правильные учетные данные
    ("user@example.com", "Aa@12345", 200),

    # Неверный email
    ("wrong_email@example.com", "Aa@12345", 401),

    # Неверный пароль
    ("user@example.com", "AaQ@12345", 401),

    # Отсутствие пароля
    ("correct_email@example.com", None, 422),

    # Отсутствие email
    (None, "CorrectPassword", 422),

    # Отсутствие и email, и пароля
    (None, None, 422),
])
async def test_login_user(async_client: AsyncClient, email, password, status_code):
    response = await async_client.post("/auth/login", json={"email": email, "password": password})

    assert response.status_code == status_code
