import os
from exceptions.develop import LoadEnvException


def getenv_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise LoadEnvException
    return value
