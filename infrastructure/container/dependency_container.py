from dependency_injector import containers, providers
from infrastructure.config.settings import Settings
from infrastructure.config.db import db
from infrastructure.persistence.repositories.sqlalchemy_blacklist_repository import SqlAlchemyBlacklistRepository
from application.services.blacklist_service import BlacklistService

class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "api.controllers.blacklist_controller"
    ])
    settings = providers.Singleton(Settings)
    blacklist_repository = providers.Singleton(SqlAlchemyBlacklistRepository)
    blacklist_service = providers.Factory(
        BlacklistService,
        repository=blacklist_repository
    )
