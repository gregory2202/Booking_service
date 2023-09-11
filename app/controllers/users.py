from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_users_services
from app.schemas.users import SUserReadMe
from app.services.users import UsersServices

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me")
def read_users_me(current_user=Depends(get_current_user),
                  users_services: UsersServices = Depends(get_users_services)) -> SUserReadMe:
    return users_services.read_users_me(current_user)
