from typing import Optional
from domain.models.blacklist import Blacklist
from domain.repositories.blacklist_repository import BlacklistRepository
from infrastructure.persistence.entities.blacklist_entity import BlacklistEntity
from infrastructure.config.db import db
from uuid import UUID

class SqlAlchemyBlacklistRepository(BlacklistRepository):
    def add(self, blacklist: Blacklist) -> None:
        entity = BlacklistEntity(
            email=blacklist.email,
            app_uuid=blacklist.app_uuid,
            blocked_reason=blacklist.blocked_reason,
            ip_address=blacklist.ip_address,
            created_at=blacklist.created_at
        )
        db.session.add(entity)
        db.session.commit()

    def get_by_email(self, email: str) -> Optional[Blacklist]:
        entity = BlacklistEntity.query.filter_by(email=email).first()
        if entity:
            return Blacklist(
                email=entity.email,
                app_uuid=entity.app_uuid,
                blocked_reason=entity.blocked_reason,
                ip_address=entity.ip_address,
                created_at=entity.created_at
            )
        return None
