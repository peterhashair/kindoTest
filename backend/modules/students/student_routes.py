from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from config.database import get_db
from . import student_model, student_service
from middlewares.response_middleware import UniformRoute

router = APIRouter(
    prefix='/students',
    tags=['Students'],
    route_class=UniformRoute
)

@router.post('/', response_model=student_model.Student)
def create_student(student: student_model.StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db=db, student=student)

@router.get('/parent/{parent_id}', response_model=List[student_model.Student])
def get_students_by_parent(parent_id: uuid.UUID, db: Session = Depends(get_db)):
    return student_service.get_students_by_parent_id(db=db, parent_id=parent_id)

@router.put('/{student_id}', response_model=student_model.Student)
def update_student(student_id: uuid.UUID, student: student_model.StudentUpdate, db: Session = Depends(get_db)):
    return student_service.update_student(db=db, student_id=student_id, student_data=student)
