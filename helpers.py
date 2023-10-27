import os
from exceptions import LoadEnvException


def getenv_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise LoadEnvException
    return value
