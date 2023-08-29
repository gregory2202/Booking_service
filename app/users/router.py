from fastapi import APIRouter, Response, Depends

from app.users.scemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import UserAlreadyExistsException, CannotAddDataToDatabase

router_auth = APIRouter(prefix="/auth", tags=["Аутентификация"])
router_users = APIRouter(prefix="/users", tags=["Пользователи"])


@router_auth.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logaut_user(response: Response):
    response.delete_cookie("booking_access_token")


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
