import asyncio
from datetime import date

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Template

from app.config import settings
from app.tasks.celery_settings import app_celery

config = ConnectionConfig(MAIL_USERNAME=settings.MAIL_USERNAME,
                          MAIL_PASSWORD=settings.MAIL_PASSWORD,
                          MAIL_FROM=settings.MAIL_FROM,
                          MAIL_PORT=settings.MAIL_PORT,
                          MAIL_SERVER=settings.MAIL_SERVER,
                          MAIL_STARTTLS=True,
                          MAIL_SSL_TLS=False,
                          USE_CREDENTIALS=True,
                          VALIDATE_CERTS=False)


@app_celery.task
def send_email(email, hotel_name: str, room_name: str, date_from: date, date_to: date,
               total_cost: int) -> None:
    data = {
        "email": email,
        "hotel_name": hotel_name,
        "check_in_date": date_from,
        "check_out_date": date_to,
        "room_type": room_name,
        "price": total_cost
    }

    with open("/Users/owner/PycharmProjects/fastApiProject/app/templates/email_template.html", "r",
              encoding="utf-8") as file:
        template_str = file.read()

    template = Template(template_str)
    html_body = template.render(data=data)

    message = MessageSchema(subject='Подтверждение бронирования', recipients=[email],
                            body=html_body,
                            subtype=MessageType.html)

    fast_email = FastMail(config)

    asyncio.run(fast_email.send_message(message))
