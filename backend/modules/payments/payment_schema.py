import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    status = Column(String, nullable=False)
    transaction_id = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default='now()', nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default='now()', onupdate='now()', nullable=False)
