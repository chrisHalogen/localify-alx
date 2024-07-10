from decouple import config


class Config:
    SECRET_KEY = config("APP_SECRET")
    SQLALCHEMY_DATABASE_URI = config("PROD_DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
