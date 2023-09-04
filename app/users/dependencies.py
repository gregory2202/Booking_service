from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.users.repository import UsersRepository
from app.users.services import UsersServices, AuthServices
from app.exceptions import (IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException,
                            UserIsNotPresentException)


def get_users_services():
    return UsersServices(UsersRepository)


def get_auth_services():
    return AuthServices(UsersRepository)


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersRepository.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
