from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.dependencies.repositories import get_users_repository
from app.exceptions.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException
)
from app.repositories.users import UsersRepository


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token),
                           repository: UsersRepository = Depends(get_users_repository)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await repository.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
