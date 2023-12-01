from schemas.session import AuthTokens, AuthTokensDb
from .jwt import TokenManager


async def create_session_tokens(
        username: str,
        user_id: int | None = None
) -> AuthTokens | AuthTokensDb:

    access_token = TokenManager.create_access_token(sub=username)
    refresh_token = TokenManager.create_refresh_token(sub=username)

    if user_id:
        auth_tokens = AuthTokensDb(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )
    else:
        auth_tokens = AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token
        )
    return auth_tokens
