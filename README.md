# Hotel Booking Service

This project is developed in Python, utilizing modern tools and practices. The service offers functionality for user
registration and authentication, as well as searching and booking hotels.

## 🛠 Technologies

- **Python**: Programming language.
- **FastAPI**: A modern, fast web framework for building reliable web applications swiftly.
- **Pydantic & SQLAlchemy**: Powerful tools for data handling, offering validation and database interaction.
- **PostgreSQL**: An object-relational database management system, used as the primary database in this project.
- **Redis**: An open-source database management system, used for caching and speeding up server response time.
- **Celery**: A platform for asynchronous task execution, particularly useful for processing background tasks.
- **Docker**: A platform for building, deploying, and running applications in containers.
- **PyTest**: A Python testing tool, offering convenient syntax for writing tests.
- **Architectural Patterns**: The project is based on the **Repository** and **Unit of Work** patterns, ensuring
  flexibility and reliability in data handling.

## Key Features

- **Authentication**: Secure registration, login, and logout.
- **Role-Based Access Control**: Users can be assigned different roles.
- **Hotel Search**: Easy hotel selection by location, check-in, and check-out dates.
- **Detailed Information**: Each hotel comes with a description, photos, and information about available rooms.
- **Email Dispatch**: Implemented automated email sending via Celery upon booking to notify the user.

## API

| Method | Function                        | URL                      |
|--------|---------------------------------|--------------------------|
| POST   | register_user                   | /auth/register           |
| POST   | login_user                      | /auth/login              |
| POST   | logout_user                     | /auth/logout             |
| GET    | read_users_me                   | /users/me                |
| GET    | get_bookings                    | /bookings                |
| POST   | add_booking                     | /bookings                |
| DELETE | remove_booking                  | /bookings/{booking_id}   |
| GET    | get_hotels_by_location_and_time | /hotels/{location}       |
| GET    | get_hotel_by_id                 | /hotels/id/{hotel_id}    |
| GET    | get_rooms_by_date               | /hotels/{hotel_id}/rooms |

## Admin Panel

Administrators and developers can interact with the database through a convenient web interface accessible at `/admin`
after the server is launched.

## Documentation

Users and developers can access the complete API documentation available at `/docs` after the server startup.

## 🚀 Application Launch

The uvicorn web server is used to run FastAPI. The launch command is as follows:

```
uvicorn app.main:app --reload
```  

This command should be run from the project's root directory.

### Celery & Flower

To launch Celery, use the command:

```
celery --app=app.tasks.celery_settings:app_celery worker -l INFO -P solo
```

Note that `-P solo` is used only on Windows as Celery has issues operating on Windows.  
For launching Flower, use:

```
celery --app=app.tasks.celery_settings:app_celery flower
``` 

### Dockerfile

To run the web server (FastAPI) inside a container, uncomment the code inside the Dockerfile and have a PostgreSQL
instance running on your computer. To run the Dockerfile, use:

```
docker build .
```  

This command is also run from the root directory where the Dockerfile is located.

### Docker Compose

To launch all services (DB, Redis, web server (FastAPI), Celery, Flower, Grafana, Prometheus), use the
docker-compose.yml file and commands:

```
docker compose build
docker compose up
```

The `build` command should only be run if you have modified the Dockerfile, i.e., changed the image building logic.

---
&copy; 2023 Hotel Booking Service