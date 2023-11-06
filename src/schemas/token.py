from pydantic import BaseModel


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
