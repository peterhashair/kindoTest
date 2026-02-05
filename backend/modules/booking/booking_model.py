from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class BookingBase(BaseModel):
    description: Optional[str] = None
    trip_id: uuid.UUID
    parent_id: uuid.UUID
    student_id: uuid.UUID

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None

class Booking(BookingBase):
    id: uuid.UUID
    total_in_cents: int
    status: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True

class BookingDetails(BaseModel):
    id: uuid.UUID
    description: Optional[str] = None
    trip_name: str
    parent_id: uuid.UUID
    student_name: str
    total_in_cents: int
    school_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True
