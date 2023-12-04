from dotenv import load_dotenv
from utils.env import getenv_variable

load_dotenv()

SECRET_KEY: str = getenv_variable('SECRET_KEY')
ALGORITHM: str = getenv_variable('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES: int = getenv_variable('ACCESS_TOKEN_EXPIRE_MINUTES', int_v=True)
REFRESH_TOKEN_EXPIRE_HOURS: int = getenv_variable('REFRESH_TOKEN_EXPIRE_HOURS', int_v=True)

POSTGRES_URI: str = getenv_variable('POSTGRES_URI')
