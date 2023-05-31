from .local import Config as _Config


class Config(_Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:r4bluv4nhr4b@localhost:3306/Final_Project"
