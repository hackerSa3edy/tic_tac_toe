from .default import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = os.getenv("DEBUG", False)
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    if SECRET_KEY is None:
        raise ValueError("No SECRET_KEY set for Flask application")

    if not os.getenv("CORS_ORIGINS", None):
        raise ValueError("No CORS_ORIGINS set for Flask application")

    CORS_CONFIG = {
        'CORS_ORIGINS' : os.getenv("CORS_ORIGINS", '').split(','),
        'CORS_METHODS': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    }
    MONGO_DB_HOSTNAME = os.getenv("MONGO_HOSTNAME", None)

    if BaseConfig.MONGO_DB_USERNAME == "":
        raise ValueError("No MONGO_DB_USERNAME set for Flask application")
    elif BaseConfig.MONGO_DB_PASSWD == "":
        raise ValueError("No MONGO_DB_PASSWD set for Flask application")
    elif BaseConfig.MONGO_DB_NAME == "":
        raise ValueError("No MONGO_DB_NAME set for Flask application")
    elif MONGO_DB_HOSTNAME is None:
        raise ValueError("No MONGO_HOSTNAME set for Flask application")

    if not BaseConfig.MONGO_URI:
        MONGO_URI = f"mongodb://{BaseConfig.MONGO_DB_USERNAME}:{BaseConfig.MONGO_DB_PASSWD}@{MONGO_DB_HOSTNAME}:27017/{BaseConfig.MONGO_DB_NAME}"
