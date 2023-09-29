from pydantic import BaseModel, ConfigDict, EmailStr


class SUserProfile(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)
