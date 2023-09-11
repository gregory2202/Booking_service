from pydantic import BaseModel


class RegisterLogoutResponse(BaseModel):
    message: str


class LoginResponse(BaseModel):
    access_token: str
