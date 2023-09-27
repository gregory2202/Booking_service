from httpx import AsyncClient
from pytest import mark


@mark.parametrize("hotel_id, status_code, result", [
    # Проверка на корректное получение данных для Гранд Отель
    (1, 200, "Гранд Отель"),

    # Проверка на корректное получение данных для Люкс Отель
    (2, 200, "Люкс Отель"),

    # Проверка на корректное получение данных для Комфорт Отель
    (3, 200, "Комфорт Отель"),

    # Проверка ответа для ID, которого нет в базе
    (4, 404, "Отель не найден"),

    # Проверка ответа для неправильного ID
    (0, 404, "Отель не найден"),

    # Проверка ответа для отрицательного ID
    (-1, 404, "Отель не найден"),
])
async def test_get_hotel_by_id(async_client: AsyncClient, hotel_id: int, status_code: int, result: str):
    response = await async_client.get(f"/hotels/id/{hotel_id}")
    assert response.status_code == status_code
    assert response.json().get("name" if status_code == 200 else "detail") == result


@mark.parametrize("location, date_from, date_to, status_code, results", [
    # День до начала бронирования: все комнаты свободны.
    ("Москва", "2023-09-10", "2023-09-14", 200,
     [{"id": 1, "name": "Гранд Отель", "rooms_left": 3}, {"id": 2, "name": "Люкс Отель", "rooms_left": 6}]),

    # Время, когда одна комната в Гранд Отеле забронирована.
    ("Москва", "2023-09-20", "2023-09-21", 200,
     [{"id": 1, "name": "Гранд Отель", "rooms_left": 2}, {"id": 2, "name": "Люкс Отель", "rooms_left": 6}]),

    # В день выезда из бронированной комнаты: комната все равно занята
    ("Москва", "2023-09-25", "2023-09-27", 200,
     [{"id": 1, "name": "Гранд Отель", "rooms_left": 2}, {"id": 2, "name": "Люкс Отель", "rooms_left": 5}]),

    # День после выезда из бронированной комнаты: комната освобождается
    ("Москва", "2023-09-26", "2023-09-28", 200,
     [{"id": 1, "name": "Гранд Отель", "rooms_left": 3}, {"id": 2, "name": "Люкс Отель", "rooms_left": 5}]),

    # Время, когда две комнаты в Комфорт Отеле забронированы. Но на 2023-10-04 одна из комнат освобождается.
    ("Казань, Кремлевская", "2023-10-01", "2023-10-03", 200, [{"id": 3, "name": "Комфорт Отель", "rooms_left": 1}]),

    # Время, когда только одна комната в Комфорт Отеле забронирована.
    ("Казань, Кремлевская", "2023-10-04", "2023-10-05", 200, [{"id": 3, "name": "Комфорт Отель", "rooms_left": 2}]),

    # Время после всех бронирований: все комнаты свободны.
    ("Казань, Кремлевская", "2023-10-11", "2023-10-12", 200, [{"id": 3, "name": "Комфорт Отель", "rooms_left": 3}]),

    # Несуществующее местоположение
    ("Новосибирск", "2023-09-21", "2023-09-22", 404, []),

    # Начальная дата после окончательной даты
    ("Москва", "2023-09-24", "2023-09-21", 400, []),

    # Начальная дата после окончательной даты
    ("Москва", "2023-10-21", "2023-09-21", 400, []),

    # Слишком долгое бронирование (более 30 дней)
    ("Москва", "2023-10-21", "2023-12-21", 400, []),

    # Слишком долгое бронирование (31 день)
    ("Москва", "2023-09-01", "2023-10-02", 400, []),
])
async def test_get_hotels_by_location_and_time(async_client: AsyncClient, location: str, date_from: str, date_to: str,
                                               status_code: int, results: list):
    response = await async_client.get(f"/hotels/{location}", params={"date_from": date_from, "date_to": date_to})
    assert response.status_code == status_code

    if status_code == 200:
        actual_hotels = response.json()
        assert len(actual_hotels) == len(results)

        for hotel in actual_hotels:
            hotel_id = hotel.get("id")
            rooms_left = hotel.get("rooms_left")

            result_hotel = next(filter(lambda x: x.get("id") == hotel_id, results))
            assert result_hotel is not None
            assert result_hotel.get("rooms_left") == rooms_left
