import uuid
from pydantic import BaseModel

# Shared properties
class SchoolBase(BaseModel):
    name: str

# Properties to receive on school creation
class SchoolCreate(SchoolBase):
    pass

# Properties to return to client
class School(SchoolBase):
    id: uuid.UUID

    class ConfigDict:
        from_attributes = True
