from pydantic import BaseModel, EmailStr, ConfigDict


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserReadMe(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
