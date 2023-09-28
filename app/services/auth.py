from datetime import datetime, timedelta

from fastapi import Response
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions.exceptions import (
    CannotAddDataToDatabase,
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
)
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.users import SUserAuth

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


class AuthServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_KEY, settings.JWT_ALGORITHM)
        return encoded_jwt

    async def authenticate_user(self, email: EmailStr, password: str):
        async with self.unit_of_work as uow:
            user = await uow.users_repository.find_one_or_none(email=email)
            if not (user and self.verify_password(password, user.hashed_password)):
                raise IncorrectEmailOrPasswordException
            return user

    async def register_user(self, user_data: SUserAuth):
        async with self.unit_of_work as uow:
            existing_user = await uow.users_repository.find_one_or_none(email=user_data.email)
            if existing_user:
                raise UserAlreadyExistsException
            hashed_password = self.get_password_hash(user_data.password)
            new_user = await uow.users_repository.add(email=user_data.email, hashed_password=hashed_password)
            if not new_user:
                raise CannotAddDataToDatabase
            return {"message": "Регистрация успешно завершена"}

    async def login_user(self, response: Response, user_data: SUserAuth):
        user = await self.authenticate_user(user_data.email, user_data.password)
        access_token = self.create_access_token({"sub": str(user.id)})
        response.set_cookie("booking_access_token", access_token, httponly=True)
        return {"access_token": access_token}

    @staticmethod
    async def logout_user(response: Response):
        response.delete_cookie("booking_access_token")
        return {"message": "Успешный выход из системы"}
