from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.exceptions import AccessException
from app.users.dependencies import get_auth_services, get_current_user

auth_services = get_auth_services()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await auth_services.authenticate_user(email, password)
        if user.role not in ("admin", "dev"):
            raise AccessException
        access_token = auth_services.create_access_token({"sub": str(user.id)})
        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        user = await get_current_user(token)
        if user.role not in ("admin", "dev"):
            raise AccessException


authentication_backend = AdminAuth(secret_key=settings.JWT_KEY)
