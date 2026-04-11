

from domain.repositories.blacklist_repository import BlacklistRepository

class BlacklistService:
    def __init__(self):
        self.repository = BlacklistRepository()

    def get_blacklist(self, email):
        return self.repository.get_by_email(email)

    def add_to_blacklist(self, email, blacklisted):
        self.repository.add({"email": email, "blacklisted": blacklisted})
