from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from config.database import get_db
from modules.trips.trip_service import get_trip_byId as get_trip_byId_service, get_trips as get_all_trips_service
from modules.trips.trip_service import create_trip as create_trip_service
from . import trip_model
from middlewares.response_middleware import UniformRoute

router = APIRouter(
    prefix="/trips",
    tags=["trips"],
    route_class=UniformRoute
)

@router.get('/', response_model=List[trip_model.TripWithSchoolName])
def get_trips(db: Session = Depends(get_db)):
    trips = get_all_trips_service(db)
    if not trips:
        return []
    
    return trips

@router.get('/{trip_id}', response_model=trip_model.TripWithSchoolName)
def get_trip_byId(trip_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(trip_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid trip ID format. Must be a valid UUID.")
    
    trip = get_trip_byId_service(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return trip

@router.post('/', response_model=trip_model.Trip)
def create_trip(trip: trip_model.TripCreate, db: Session = Depends(get_db)):
    new_trip = create_trip_service(db, trip)
    return new_trip
