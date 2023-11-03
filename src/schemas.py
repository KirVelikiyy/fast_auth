from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = True
    is_admin: bool | None = False


class UserDbSchema(UserSchema):
    user_id: int
    added_at: datetime

    class Config:
        orm_mode = True


class CreateUserSchema(UserSchema):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


