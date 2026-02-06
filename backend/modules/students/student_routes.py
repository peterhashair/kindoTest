from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uuid
from config.database import get_db
from config.response import APIResponse
from . import student_model, student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "/",
    response_model=APIResponse[student_model.Student],
    responses={422: {"model": APIResponse[None]}},
)
def create_student(student: student_model.StudentCreate, db: Session = Depends(get_db)):
    try:
        student = student_service.create_student(db=db, student=student)
        return APIResponse(status="success", data=student, error=None)
    except Exception as e:
        raise JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )


@router.get(
    "/parent/{parent_id}",
    response_model=APIResponse[List[student_model.Student]],
    responses={422: {"model": APIResponse[None]}},
)
def get_students_by_parent(parent_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        students = student_service.get_students_by_parent_id(db=db, parent_id=parent_id)
        return APIResponse(status="success", data=students, error=None)
    except Exception as e:
        raise JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )


@router.put(
    "/{student_id}",
    response_model=APIResponse[student_model.Student],
    responses={422: {"model": APIResponse[None]}},
)
def update_student(
    student_id: uuid.UUID,
    student: student_model.StudentUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_student = student_service.update_student(
            db=db, student_id=student_id, student_data=student
        )
        return APIResponse(status="success", data=updated_student, error=None)
    except Exception as e:
        raise JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )
