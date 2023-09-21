from fastapi import APIRouter, Response, Depends

from app.dependencies.services import get_auth_services
from app.schemas.auth import LoginResponse, RegisterLogoutResponse
from app.schemas.users import SUserAuth
from app.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth,
                        auth_services: AuthServices = Depends(get_auth_services)) -> RegisterLogoutResponse:
    return await auth_services.register_user(user_data)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth,
                     auth_services: AuthServices = Depends(get_auth_services)) -> LoginResponse:
    return await auth_services.login_user(response, user_data)


@router.post("/logout")
async def logout_user(response: Response,
                      auth_services: AuthServices = Depends(get_auth_services)) -> RegisterLogoutResponse:
    return await auth_services.logaut_user(response)
