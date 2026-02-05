from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from middlewares.response_middleware import UniformRoute
from modules.schools.school_service import get_schools as get_all_schools_service
from . import school_model

router = APIRouter(
    prefix='/schools',
    tags=['schools'],
    route_class=UniformRoute
)

@router.get('/', response_model=List[school_model.School])
def get_schools(db: Session = Depends(get_db)):
    schools = get_all_schools_service(db)
    if not schools:
        return []
    
    return schools