
from datetime import date
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from . import trip_schema, trip_model
from modules.schools.school_service import byId as get_school_byId
from modules.schools.school_schema import School
from typing import List

def get_trips(db: Session) -> List[trip_model.TripWithSchoolName]: 
    trips_with_schools = db.query(trip_schema.Trip, School.name.label("school_name")).join(School, trip_schema.Trip.school_id == School.id).filter(
        trip_schema.Trip.published == True, 
        trip_schema.Trip.start_date > date.today()
     ).all()

    return [
        trip_model.TripWithSchoolName(
            id=trip.id,
            name=trip.name,
            description=trip.description,
            destination=trip.destination,
            school_id=trip.school_id,
            price_in_cents=trip.price_in_cents,
            start_date=trip.start_date,
            end_date=trip.end_date,
            published=trip.published,
            school_name=school_name
        ) for trip, school_name in trips_with_schools
    ]    


def get_trip_byId(db: Session, trip_id) -> trip_model.TripWithSchoolName:
    trip_with_school = db.query(trip_schema.Trip, School.name.label("school_name")).join(School, trip_schema.Trip.school_id == School.id).filter(
        trip_schema.Trip.id == trip_id
    ).first()
    if not trip_with_school:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip, school_name = trip_with_school
    return trip_model.TripWithSchoolName(
        id=trip.id,
        name=trip.name,
        description=trip.description,
        destination=trip.destination,
        school_id=trip.school_id,
        price_in_cents=trip.price_in_cents,
        start_date=trip.start_date,
        end_date=trip.end_date,
        published=trip.published,
        school_name=school_name,

    )

def create_trip(db: Session, trip: trip_model.TripCreate) -> trip_schema.Trip:
    # Check if school exists
    school = get_school_byId(db, trip.school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School with the provided ID does not exist.")

    new_trip = trip_schema.Trip(**trip.model_dump())
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip


def byId(trip_id):
    pass

def update(trip_id, trip_data):
    pass

def delete(trip_id):
    pass