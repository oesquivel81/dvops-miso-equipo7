from typing import Optional
from domain.models.blacklist import Blacklist
from domain.repositories.blacklist_repository import BlacklistRepository
from datetime import datetime
from uuid import UUID

class BlacklistService:
    def __init__(self, repository: BlacklistRepository):
        self.repository = repository

    def add_to_blacklist(self, email: str, app_uuid: UUID, blocked_reason: Optional[str], ip_address: str) -> None:
        blacklist = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip_address=ip_address,
            created_at=datetime.utcnow()
        )
        self.repository.add(blacklist)

    def get_blacklist(self, email: str) -> Optional[Blacklist]:
        return self.repository.get_by_email(email)
