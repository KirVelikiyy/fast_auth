import os
from exceptions.develop import LoadEnvException


development_variables = {
    "POSTGRES_URI": "DEV_POSTGRES_URI"
}


def is_development_platform(*args, **kwargs) -> bool:
    return os.name == 'nt'


def development_env(wrapper):
    """
    function-decorator for replace env variables in development
    """
    def check_getenv_variable(key: str, *args, **kwargs):
        if is_development_platform():
            key = development_variables.get(key) or key
        return wrapper(key, *args, **kwargs)

    return check_getenv_variable


@development_env
def getenv_variable(key: str, int_v: bool = False) -> str | int:
    value = os.getenv(key)
    if not value:
        raise LoadEnvException
    if int_v:
        return int(value)
    return value
