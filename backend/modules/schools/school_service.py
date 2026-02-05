

from typing import List
from modules.schools import school_schema
from sqlalchemy.orm import Session

def get_schools(db: Session) -> List[school_schema.School]: 
    return db.query(school_schema.School).all()


def byId(db: Session, school_id):
    return db.query(school_schema.School).filter(school_schema.School.id == school_id).first()