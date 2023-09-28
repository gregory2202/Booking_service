from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.dependencies.unit_of_work import get_unit_of_work
from app.exceptions.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.interfaces.unit_of_work import IUnitOfWork


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(unit_of_work: IUnitOfWork = Depends(get_unit_of_work), token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    async with unit_of_work as uow:
        user = await uow.users_repository.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
