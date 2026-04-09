import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/blacklist_db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "jwtsecret")
    BEARER_TOKEN: str = os.getenv("BEARER_TOKEN", "fixedtoken")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))
