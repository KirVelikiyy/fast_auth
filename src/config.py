from dotenv import load_dotenv
from utils.env import getenv_variable

load_dotenv()

SECRET_KEY = getenv_variable('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24

POSTGRES_URI = getenv_variable('POSTGRES_URI')
