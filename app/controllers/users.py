from fastapi import APIRouter, Response, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_users_services, get_auth_services
from app.schemas.users import SUserAuth, SUserReadMe
from app.services.auth import AuthServices
from app.services.users import UsersServices

router_auth = APIRouter(prefix="/auth", tags=["Аутентификация"])
router_users = APIRouter(prefix="/users", tags=["Пользователи"])


@router_auth.post("/register")
async def register_user(user_data: SUserAuth, auth_services: AuthServices = Depends(get_auth_services)):
    await auth_services.register_user(user_data)


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth,
                     auth_services: AuthServices = Depends(get_auth_services)):
    return await auth_services.login_user(response, user_data)


@router_auth.post("/logout")
async def logaut_user(response: Response, auth_services: AuthServices = Depends(get_auth_services)):
    await auth_services.logaut_user(response)


@router_users.get("/me")
def read_users_me(current_user=Depends(get_current_user),
                  users_services: UsersServices = Depends(get_users_services)) -> SUserReadMe:
    return users_services.read_users_me(current_user)
