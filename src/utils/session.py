from schemas.session import AuthTokens, AuthTokensDb
from .jwt import TokenManager


async def create_session_tokens(
        username: str,
) -> AuthTokens | AuthTokensDb:

    access_token = TokenManager.create_access_token(sub=username)
    refresh_token = TokenManager.create_refresh_token(sub=username)

    auth_tokens = AuthTokensDb(
        username=username,
        access_token=access_token,
        refresh_token=refresh_token
    )

    return auth_tokens
