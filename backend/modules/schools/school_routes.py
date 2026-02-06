from fastapi.responses import JSONResponse
from config.response import APIResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from modules.schools.school_service import get_schools as get_all_schools_service
from . import school_model

router = APIRouter(
    prefix="/schools",
    tags=["Schools"],
)


@router.get(
    "/",
    response_model=APIResponse[List[school_model.School]],
    responses={422: {"model": APIResponse[None]}},
)
def get_schools(db: Session = Depends(get_db)):
    try:
        schools = get_all_schools_service(db)
        if not schools:
            # don't want to error out on the first screen, just return an empty list if there are no schools
            return APIResponse(status="success", data=[], error="")

        return APIResponse(status="success", data=schools, error="")
    except Exception as e:
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )
