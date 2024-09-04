from .default import BaseConfig
import os

class DevelopmentConfig(BaseConfig):
    HOSTNAME = os.getenv("HOST_NAME", None)
    APP_PORT = os.getenv("APP_PORT", None)

    if HOSTNAME is None:
        raise ValueError("No HOST_NAME set for Flask application")
    elif APP_PORT is None:
        raise ValueError("No APP_PORT set for Flask application")

    DEBUG = os.getenv("DEBUG", True)
    SECRET_KEY = os.getenv("SECRET_KEY", "Flask-tic_tac_toe")
    CORS_CONFIG = {
        'CORS_ORIGINS' : os.getenv("CORS_ORIGINS", '*').split(','),
        'CORS_METHODS': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE']
    }
    MONGO_DB_HOSTNAME = os.getenv("MONGO_HOSTNAME", 'localhost')

    if BaseConfig.MONGO_DB_USERNAME != "" and BaseConfig.MONGO_DB_PASSWD != "":
        credentials = f"{BaseConfig.MONGO_DB_USERNAME}:{BaseConfig.MONGO_DB_PASSWD}@"
    else:
        credentials = ""

    if not BaseConfig.MONGO_URI:
        MONGO_URI = f"mongodb://{credentials}{MONGO_DB_HOSTNAME}:27017/{BaseConfig.MONGO_DB_NAME}"
