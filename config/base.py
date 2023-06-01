import logging


class BaseConfig:
    ENVIRONMENT: str
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:r4bluv4nhr4b@localhost/Final_Project"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "max_overflow": 0,
        "pool_size": 0,
        "echo": False,
    }

    JWT_SECRET_KEY = "just_a_secret_key"
