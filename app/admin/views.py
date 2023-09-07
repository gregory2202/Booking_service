from sqladmin import ModelView

from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class UsersAdmin(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"

    column_list = [Users.id, Users.email]
    column_details_list = [Users.id, Users.email, Users.bookings]
    column_labels = {Users.id: "ID", Users.email: "Email", Users.bookings: "Бронирования"}
    page_size = 25

    can_delete = False


class BookingsAdmin(ModelView, model=Bookings):
    name = "Бронь"
    name_plural = "Бронирования"
    icon = "fa-solid fa-book"

    column_list = [Bookings.id, Bookings.user, Bookings.date_from, Bookings.date_to, Bookings.total_days,
                   Bookings.total_cost]
    column_details_list = [Bookings.id, Bookings.user, Bookings.room, Bookings.date_from, Bookings.date_to,
                           Bookings.total_days,
                           Bookings.total_cost]
    column_labels = {Bookings.id: "ID", Bookings.user: "Пользователь", Bookings.date_from: "Дата заезда",
                     Bookings.date_to: "Дата выезда", Bookings.total_cost: "Стоимость",
                     Bookings.total_days: "Колличество дней", Bookings.room: "Номер"}
    page_size = 25


class HotelsAdmin(ModelView, model=Hotels):
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"

    column_list = [Hotels.id, Hotels.name, Hotels.location]
    column_details_list = [Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms,
                           Hotels.rooms_quantity, Hotels.image_id]
    column_labels = {Hotels.id: "ID", Hotels.name: "Отель", Hotels.location: "Расположение отеля",
                     Hotels.services: "Удобства", Hotels.rooms: "Номера", Hotels.rooms_quantity: "Количество номеров",
                     Hotels.image_id: "Фото отеля"}
    page_size = 25


class RoomsAdmin(ModelView, model=Rooms):
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"

    column_list = [Rooms.id, Rooms.name, Rooms.hotel, Rooms.price]
    column_details_list = [Rooms.id, Rooms.name, Rooms.description, Rooms.services, Rooms.price,
                           Rooms.quantity, Rooms.image_id, Rooms.hotel, Rooms.bookings]
    column_labels = {Rooms.id: "ID", Rooms.name: "Номер", Rooms.description: "Описание", Rooms.services: "Удобства",
                     Rooms.price: "Стоимость (ночь)", Rooms.quantity: "Количество номеров",
                     Rooms.image_id: "Фото номера", Rooms.hotel: "Отель", Rooms.bookings: "Бронирования номера"}
    page_size = 25
