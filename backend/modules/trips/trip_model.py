import uuid
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

# Shared properties
class TripBase(BaseModel):
    name: str
    description: Optional[str] = Field(None, max_length=255)
    destination: str
    school_id: uuid.UUID
    price_in_cents: int = Field(..., gt=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    published: bool = True

# Properties to receive on trip creation
class TripCreate(TripBase):
    @model_validator(mode='after')
    def check_dates(self):
        start_date = self.start_date
        end_date = self.end_date
        if start_date and end_date and end_date <= start_date:
            raise ValueError('end date must be later than start date')
        return self
    
    @model_validator(mode='after')
    def check_price(self):
        if self.price_in_cents <= 0:
            raise ValueError('price must be a positive integer')
        return self

# Properties to return to client
class Trip(TripBase):
    id: uuid.UUID
    
    class ConfigDict:
        from_attributes = True

class TripWithSchoolName(TripBase):
    id: uuid.UUID
    school_name: str

    class ConfigDict:
        from_attributes = True
