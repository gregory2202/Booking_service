from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default="user")

    bookings: Mapped["Bookings"] = relationship(back_populates="user")  # type: ignore  # noqa

    def __str__(self):
        return f"Пользователь {self.email}"
