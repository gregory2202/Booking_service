from httpx import AsyncClient
from pytest import mark


@mark.parametrize("email, password, status_code", [
    # Правильные данные
    ("newuser@example.com", "Aa@12345", 201),

    # Существующий пользователь
    ("newuser@example.com", "Aa@12345", 409),
    ("newuser@example.com", "DifferentPass@1", 409),

    # Длина пароля меньше 8 символов
    ("test@example.com", "Aa@123", 422),

    # Неверный формат электронной почты
    ("testexample.com", "Aa@12345", 422),
    ("test@", "Aa@12345", 422),
    ("@example.com", "Aa@12345", 422),

    # Отсутствие цифры
    ("test@example.com", "Aa@abcdef", 422),

    # Отсутствие буквы
    ("test@example.com", "@1234567", 422),

    # Отсутствие заглавной буквы
    ("test@example.com", "a@1234567", 422),

    # Отсутствие специального символа
    ("test@example.com", "Aa1234567", 422),

    # Повторяющиеся символы подряд
    ("test@example.com", "Aaa@1234", 422),

    # Популярные слова в пароле
    ("test@example.com", "Aa@123password", 422),
    ("test@example.com", "Aa@123qwerty", 422),
    ("test@example.com", "Aa@123admin", 422),

    # Электронная почта с пробелами (пробелы до и после удаляются)
    (" newuser1@example.com", "Aa@12345", 201),
    ("newuser2@example.com ", "Aa@12345", 201),
    ("test @example.com", "Aa@12345", 422),

    # Очень длинный пароль
    ("test@example.com", "Aa@12345" * 8, 422),
])
async def test_register_user(async_client: AsyncClient, email: str, password: str, status_code: int):
    response = await async_client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == status_code


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
async def test_login_user(async_client: AsyncClient, email: str, password: str, status_code: int):
    response = await async_client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code


async def test_logout_user(auth_async_client: AsyncClient):
    await auth_async_client.post("/auth/logout")
    assert not auth_async_client.cookies.get("booking_access_token")
