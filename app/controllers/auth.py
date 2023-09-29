from fastapi import APIRouter, Depends, Response

from app.dependencies.services import get_auth_services
from app.schemas.auth import (
    SLoginResponse,
    SLogoutResponse,
    SRegisterResponse,
    SUserLogin,
    SUserRegister,
)
from app.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", status_code=201)
async def register_user(user_data: SUserRegister,
                        auth_services: AuthServices = Depends(get_auth_services)) -> SRegisterResponse:
    return await auth_services.register_user(user_data)


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin,
                     auth_services: AuthServices = Depends(get_auth_services)) -> SLoginResponse:
    return await auth_services.login_user(response, user_data)


@router.post("/logout")
async def logout_user(response: Response,
                      auth_services: AuthServices = Depends(get_auth_services)) -> SLogoutResponse:
    return await auth_services.logout_user(response)
