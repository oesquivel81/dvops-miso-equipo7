from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from infrastructure.config.settings import Settings

db = SQLAlchemy()

def init_db(app: Flask, settings: Settings) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
