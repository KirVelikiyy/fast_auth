from dotenv import load_dotenv
from helpers import getenv_variable

load_dotenv()

SECRET_KEY = getenv_variable('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
