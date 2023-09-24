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
async def test_register_user(async_client: AsyncClient, email, password, status_code):
    response = await async_client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == status_code
