from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import logging
from config.database import get_db
from sqlalchemy.orm import Session
from config.response import APIResponse
from modules.parents import parent_model, parent_schema


router = APIRouter(
    prefix="/parents",
    tags=["Parents"],
)


@router.get("/", response_model=APIResponse[list[parent_model.Parent]])
def get_parents(db: Session = Depends(get_db)):
    try:
        parents = db.query(parent_schema.Parent).all()
        return APIResponse(
            status="success",
            data=parents,
        )
    except Exception as e:
        logging.error(f"Error fetching parents: {str(e)}")
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", error=str(e)).model_dump(),
        )
