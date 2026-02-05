from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from . import student_schema, student_model
from modules.parents.parent_schema import Parent
from typing import List
import uuid

def create_student(db: Session, student: student_model.StudentCreate) -> student_schema.Student:
    parents = db.query(Parent).filter(Parent.id.in_(student.parent_ids)).all()
    if len(parents) != len(student.parent_ids):
        raise HTTPException(status_code=404, detail="One or more parents not found")

    new_student = student_schema.Student(
        name=student.name,
        gender=student.gender,
        dob=student.dob
    )
    
    new_student.parents.extend(parents)
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_students_by_parent_id(db: Session, parent_id: uuid.UUID) -> List[student_schema.Student]:
    parent = db.query(Parent).filter(Parent.id == parent_id).options(joinedload(Parent.students)).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent.students

def update_student(db: Session, student_id: uuid.UUID, student_data: student_model.StudentUpdate) -> student_schema.Student:
    student = db.query(student_schema.Student).filter(student_schema.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student_data.dict(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student
