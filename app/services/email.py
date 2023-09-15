from app.interfaces.unit_of_work import IUnitOfWork
from app.tasks.tasks import send_email


class EmailServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    async def send_booking_confirmation_email(self, booking_id: int):
        async with self.unit_of_work as uow:
            booking_data = await uow.bookings_repository.find_data_for_mail(booking_id)
            send_email.delay(**booking_data)
