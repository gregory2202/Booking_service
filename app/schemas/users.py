from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserReadMe(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
