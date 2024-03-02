import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None


def init_db(app: Flask):
    global db
    db = SQLAlchemy(app)


def generate_database_uri() -> str:
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]

    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_NAME = os.environ["DB_NAME"]

    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"