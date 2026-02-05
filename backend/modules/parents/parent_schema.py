import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from config.database import Base
from modules.students.student_schema import student_parent_association

class Parent(Base):
    __tablename__ = "parents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    students = relationship(
        "Student",
        secondary=student_parent_association,
        back_populates="parents"
    )

