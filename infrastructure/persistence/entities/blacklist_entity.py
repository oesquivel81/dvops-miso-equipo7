from datetime import datetime
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.config.db import db
import uuid

class BlacklistEntity(db.Model):
    __tablename__ = "blacklists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, index=True)
    app_uuid = Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
