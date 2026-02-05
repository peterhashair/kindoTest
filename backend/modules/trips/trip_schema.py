import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base

class Trip(Base):
    __tablename__ = "trips"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    destination = Column(String, nullable=False)
    
    # Assuming your schools table is named 'schools' and its primary key is 'id'
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    
    price_in_cents = Column(Integer, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    published = Column(Boolean, server_default='TRUE', nullable=False)