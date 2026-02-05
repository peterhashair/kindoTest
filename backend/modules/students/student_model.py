from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import date

class StudentBase(BaseModel):
    name: str
    gender: Optional[str] = None
    dob: date

class StudentCreate(StudentBase):
    parent_ids: List[uuid.UUID]

class StudentUpdate(StudentBase):
    pass

class Student(StudentBase):
    id: uuid.UUID
    
    class ConfigDict:
        from_attributes = True
