from fastapi import HTTPException, status


class HTTPResponseException:
    """ Use methods with raise syntax

        Example:
            raise ResponseException.user_exists()

    """
    @staticmethod
    def user_already_exists():
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with that e-mail or username already exists'
        )

    @staticmethod
    def invalid_credentials():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def inactive_user():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    @staticmethod
    def incorrect_username_or_pass():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def invalid_refresh_token():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )
