import uuid
from pydantic import BaseModel


# Shared properties
class ParentBase(BaseModel):
    name: str
    email: str


# Properties to receive on school creation
class ParentCreate(ParentBase):
    pass


# Properties to return to client
class Parent(ParentBase):
    id: uuid.UUID

    class ConfigDict:
        from_attributes = True
