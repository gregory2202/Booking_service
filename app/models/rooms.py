
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    bookings: Mapped["Bookings"] = relationship(back_populates="room")  # type: ignore  # noqa
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")  # type: ignore  # noqa

    def __str__(self) -> str:
        return f"Номер {self.name}"
