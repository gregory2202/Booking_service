from httpx import AsyncClient
from pytest import mark


async def login_user(async_client: AsyncClient, email: str, password: str):
    if email and password:
        login_response = await async_client.post("/auth/login", json={"email": email, "password": password})
        assert login_response.status_code == 200


@mark.parametrize("email, password, status_code, expected_id", [
    # Базовый сценарий
    ("user@example.com", "Aa@12345", 200, [1, 5]),

    # Базовый сценарий 2
    ("dev@example.com", "Aa@12345", 200, [2, 3, 6]),

    # Пользователь без бронирований
    ("empty@example.com", "Aa@12345", 200, []),

    # Неавторизованный пользователь
    (None, None, 401, None),
])
async def test_get_bookings(async_client: AsyncClient, email: str, password: str, status_code: int, expected_id: list):
    await login_user(async_client, email, password)

    response = await async_client.get("/bookings")
    assert response.status_code == status_code

    if status_code == 200 and expected_id:
        actual_id = [booking["id"] for booking in response.json()]
        assert sorted(expected_id) == sorted(actual_id)


@mark.parametrize("email, password, status_code, booking_data, count_booking", [
    # Успешное добавление нового бронирования пользователем
    ("user@example.com", "Aa@12345", 200,
     {"room_id": 1, "date_from": "2023-10-15", "date_to": "2023-10-17"}, 1),

    # Успешное добавление нового бронирования пользователем граничные даты
    ("user@example.com", "Aa@12345", 200,
     {"room_id": 1, "date_from": "2023-09-17", "date_to": "2023-09-19"}, 1),

    # Успешное добавление нового бронирования пользователем граничные даты
    ("user@example.com", "Aa@12345", 200,
     {"room_id": 1, "date_from": "2023-09-26", "date_to": "2023-09-28"}, 1),

    # Попытка забронировать номер, который уже забронирован на эти даты
    ("user@example.com", "Aa@12345", 409,
     {"room_id": 1, "date_from": "2023-09-21", "date_to": "2023-09-24"}, 0),

    # Попытка забронировать номер неавторизованным пользователем
    (None, None, 401,
     {"room_id": 3, "date_from": "2023-11-01", "date_to": "2023-11-05"}, 0),

    # Попытка забронировать номер, который не существует
    ("user@example.com", "Aa@12345", 404,
     {"room_id": 10, "date_from": "2023-11-01", "date_to": "2023-11-05"}, 0),

    # Дата заезда позже даты выезда
    ("user@example.com", "Aa@12345", 400,
     {"room_id": 1, "date_from": "2023-11-05", "date_to": "2023-11-01"}, 0),

    # Слишком долгое бронирование
    ("user@example.com", "Aa@12345", 400,
     {"room_id": 2, "date_from": "2023-11-01", "date_to": "2023-12-05"}, 0),
])
async def test_add_booking(async_client: AsyncClient, email: str, password: str, status_code: int, booking_data: dict,
                           count_booking: int):
    await login_user(async_client, email, password)

    initial_bookings_response = await async_client.get("/bookings")
    initial_bookings_count = len(initial_bookings_response.json())

    response = await async_client.post("/bookings", json=booking_data)
    assert response.status_code == status_code

    final_bookings_response = await async_client.get("/bookings")
    final_bookings_count = len(final_bookings_response.json())

    assert final_bookings_count - initial_bookings_count == count_booking


@mark.parametrize("email, password, status_code, booking_id", [
    # Успешное удаление одного бронирования пользователем
    ("user@example.com", "Aa@12345", 200, [1]),

    # Успешное удаление нескольких бронирований пользователем
    ("dev@example.com", "Aa@12345", 200, [2, 3, 6]),

    # Попытка удаления бронирования без авторизации
    (None, None, 401, []),

    # Попытка удаления несуществующего бронирования
    ("empty@example.com", "Aa@12345", 404, []),
])
async def test_remove_booking(async_client: AsyncClient, email: str, password: str, status_code: int, booking_id: list):
    await login_user(async_client, email, password)

    initial_bookings_response = await async_client.get("/bookings")
    initial_bookings_count = len(initial_bookings_response.json())

    for i in booking_id:
        response = await async_client.delete(f"/bookings/{i}")
        assert response.status_code == status_code

    final_bookings_response = await async_client.get("/bookings")
    final_bookings_count = len(final_bookings_response.json())

    assert initial_bookings_count - final_bookings_count == len(booking_id)
