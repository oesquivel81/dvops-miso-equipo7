import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

from flask import Flask

from infrastructure.container.dependency_container import DependencyContainer
from infrastructure.config.settings import Settings
from api.controllers.blacklist_controller import blueprint as blacklist_blueprint
from infrastructure.security.auth import auth_middleware
from infrastructure.config.error_handler import register_error_handlers
from infrastructure.config.db import init_db

container = DependencyContainer()
settings = container.settings()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)
    init_db(app, settings)
    app.register_blueprint(blacklist_blueprint)
    app.before_request(auth_middleware)
    register_error_handlers(app)
    return app

app = create_app()

if __name__ == "__main__":
    logging.info(f"Starting Flask app on {settings.HOST}:{settings.PORT}")
    app.run(host=settings.HOST, port=settings.PORT)
