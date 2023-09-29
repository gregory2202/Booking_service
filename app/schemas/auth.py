import re

from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password(password: str) -> str:
    _black_list = ["password", "123456", "qwerty", "abc123", "admin", "welcome", "superman", "iloveyou",
                   "123456789"]

    if not any(char.isdigit() for char in password):
        raise ValueError("Пароль должен содержать хотя бы одну цифру.")

    if not any(char.isalpha() for char in password):
        raise ValueError("Пароль должен содержать хотя бы одну букву.")

    if not any(char.isupper() for char in password):
        raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")

    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/~" for char in password):
        raise ValueError("Пароль должен содержать хотя бы один специальный символ.")

    if re.search(r"(.)\1{2,}", password, flags=re.IGNORECASE):
        raise ValueError("В пароле не должно быть трех и более идущих подряд одинаковых символов.")

    if any(word in password.lower() for word in _black_list):
        raise ValueError("Пароль не должен включать в себя известные или часто используемые слова и комбинации.")

    return password


class SUserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        return validate_password(password)


class SUserRegister(SUserLogin):
    pass


class SPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, password: str) -> str:
        return validate_password(password)


class SRegisterResponse(BaseModel):
    message: str


class SLoginResponse(SRegisterResponse):
    access_token: str


class SLogoutResponse(SRegisterResponse):
    pass
