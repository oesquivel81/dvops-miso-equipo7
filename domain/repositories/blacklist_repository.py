from abc import ABC, abstractmethod
from typing import Optional
from domain.models.blacklist import Blacklist

class BlacklistRepository(ABC):
    @abstractmethod
    def add(self, blacklist: Blacklist) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Blacklist]:
        pass
