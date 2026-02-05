from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.orm import Session
from modules.parents import parent_schema
from middlewares.response_middleware import UniformRoute


router = APIRouter(
    prefix='/parents',
    tags=['Parents'],
    route_class=UniformRoute
)

@router.get('/')
def get_parents(db: Session = Depends(get_db)):
    parents = db.query(parent_schema.Parent).all()
    if not parents:
        return {"message": "No parents found"}
    
    return parents