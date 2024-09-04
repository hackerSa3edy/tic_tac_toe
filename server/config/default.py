import os
from dotenv import load_dotenv

load_dotenv()
class BaseConfig:
    MONGO_DB_NAME = os.getenv("MONGO_DATABASE", "")
    MONGO_DB_USERNAME = os.getenv("MONGO_NON_ROOT_USERNAME", "")
    MONGO_DB_PASSWD = os.getenv("MONGO_NON_ROOT_PASSWORD", "")

    CORS_SUPPORTS_CREDENTIALS = os.getenv("CORS_SUPPORTS_CREDENTIALS", 'false')
    SAMESITE_POLICY = os.getenv("SESSION_COOKIE_SAMESITE", 'Lax')
    MONGO_URI = os.getenv("MONGO_URI", None)
