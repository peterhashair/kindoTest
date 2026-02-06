from config.error_exception import ExceptionError
from config.response import APIResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from config.database import get_db
from modules.trips.trip_service import (
    get_trip_byId as get_trip_byId_service,
    get_trips as get_all_trips_service,
)
from modules.trips.trip_service import create_trip as create_trip_service
from . import trip_model
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/trips",
    tags=["trips"],
)


@router.get(
    "/",
    response_model=APIResponse[List[trip_model.TripWithSchoolName]],
    responses={422: {"model": APIResponse[None]}},
)
def get_trips(db: Session = Depends(get_db)):
    try:
        trips = get_all_trips_service(db)
        if not trips:
            return APIResponse(status="success", data=[], error="")

        return APIResponse(status="success", data=trips, error="")
    except (ValueError, ExceptionError) as e:
        return JSONResponse(
            status_code=e.status_code,
            content=APIResponse(status="error", data=None, error=e.detail).dict(),
        )


@router.get(
    "/{trip_id}",
    response_model=APIResponse[trip_model.TripWithSchoolName],
    responses={422: {"model": APIResponse[None]}},
)
def get_trip_byId(trip_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(trip_id)
    except ValueError:
        return JSONResponse(
            status_code=422,
            content=APIResponse(
                status="error",
                data=None,
                error="Invalid trip ID format. Must be a valid UUID.",
            ).dict(),
        )

    trip = get_trip_byId_service(db, trip_id)
    if not trip:
        return JSONResponse(
            status_code=404,
            content=APIResponse(
                status="error", data=None, error="Trip not found"
            ).dict(),
        )

    return APIResponse(status="success", data=trip, error="")


@router.post("/", response_model=APIResponse[trip_model.Trip])
def create_trip(trip: trip_model.TripCreate, db: Session = Depends(get_db)):
    try:
        new_trip = create_trip_service(db, trip)
        return APIResponse(status="success", data=new_trip, error="")
    except (ValueError, ExceptionError) as e:
        return JSONResponse(
            status_code=422,
            content=APIResponse(status="error", data=None, error=str(e)).dict(),
        )
