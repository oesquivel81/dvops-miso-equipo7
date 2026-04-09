from infrastructure.config.db import db
from infrastructure.persistence.entities.blacklist_entity import BlacklistEntity
from flask import Flask
from infrastructure.config.settings import Settings

def create_all_tables():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Settings.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Tablas creadas correctamente.")

if __name__ == "__main__":
    create_all_tables()
