import uuid
from sqlalchemy import Column, String, TIMESTAMP, Date, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

student_parent_association = Table(
    'student_parent_association', Base.metadata,
    Column('student_id', UUID(as_uuid=True), ForeignKey('students.id')),
    Column('parent_id', UUID(as_uuid=True), ForeignKey('parents.id'))
)

class Student(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    dob = Column(Date, nullable=False)
    createdAt = Column(TIMESTAMP, default=datetime.utcnow)
    updatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    parents = relationship(
        "Parent",
        secondary=student_parent_association,
        back_populates="students"
    )
