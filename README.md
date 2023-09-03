# Сервис Бронирования Отелей

Данный проект был разработан в рамках изучения веб-разработки на Python с использованием современных
инструментов и практик. Сервис предоставляет функциональность для регистрации и аутентификации пользователей, а также
поиска и бронирования отелей.

## 🛠 Технологии

- **Python**: язык программирования.
- **FastAPI**: современный, быстрый веб-фреймворк, который позволяет быстро создавать надежные веб-приложения.
- **Pydantic & SQLAlchemy**: мощные инструменты для работы с данными, обеспечивающие валидацию и взаимодействие с базами
  данных.
- **PostgreSQL**: объектно-реляционная система управления базами данных. Используется в проекте в качестве основной базы
  данных.
- **Redis**: система управления базами данных с открытым исходным кодом, используется для кеширования и ускорения
  времени ответа сервера.
- **Celery**: платформа для асинхронного выполнения задач, особенно полезная для обработки задач в фоновом режиме.
- **Docker**: платформа для создания, развертывания и запуска приложений в контейнерах.

## Основные возможности

- **Аутентификация**: безопасная регистрация, вход и выход из системы.
- **Поиск отеля**: удобный выбор отеля по локации, датам прибытия и отъезда.
- **Детальная информация**: каждый отель снабжен описанием, фотографиями и информацией о доступных комнатах.

## API

| Метод | Функция                         | URL                      |
|-------|---------------------------------|--------------------------|
| POST  | register_user                   | /auth/register           |
| POST  | login_user                      | /auth/login              |
| POST  | logout_user                     | /auth/logout             |
| GET   | read_users_me                   | /users/me                |
| GET   | get_bookings                    | /bookings                |
| POST  | add_booking                     | /bookings                |
| POST  | remove_booking                  | /bookings/{booking_id}   |
| GET   | get_hotels_by_location_and_time | /hotels/{location}       |
| GET   | get_hotel_by_id                 | /hotels/id/{hotel_id}    |
| GET   | get_rooms_by_date               | /hotels/{hotel_id}/rooms |

## Документация

Пользователи и разработчики могут ознакомиться с полной документацией API, доступной по пути `/docs` после запуска
сервера.

## 🚀 Запуск приложения

Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:

```
uvicorn app.main:app --reload
```  

Ее необходимо запускать в командной строке, обязательно находясь в корневой директории проекта.

### Celery & Flower

Для запуска Celery используется команда

```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```

Обратите внимание, что `-P solo` используется только на Windows, так как у Celery есть проблемы с работой на Windows.  
Для запуска Flower используется команда

```
celery --app=app.tasks.celery:celery flower
``` 

### Dockerfile

Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже
запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:

```
docker build .
```  

Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

### Docker compose

Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать
файл docker-compose.yml и команды

```
docker compose build
docker compose up
```

Причем `build` команду нужно запускать, только если вы меняли что-то внутри Dockerfile, то есть меняли логику
составления образа.

---
&copy; 2023 Hotel Booking Service