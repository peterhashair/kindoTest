from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from config.database import get_db
from middlewares.response_middleware import UniformRoute
from . import booking_model, booking_service

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
    route_class=UniformRoute
)

@router.post("/", response_model=booking_model.BookingDetails)
def get_or_create_booking(booking: booking_model.BookingCreate, db: Session = Depends(get_db)):
    return booking_service.get_or_create_booking(db=db, booking=booking)

@router.get('/{booking_id}', response_model=booking_model.BookingDetails)
def get_booking(booking_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        return booking_service.get_booking_details(db=db, booking_id=booking_id)
    except HTTPException as e:
        raise e

@router.get('/parent/{parent_id}', response_model=list[booking_model.BookingDetails])
def get_bookings_by_parent(parent_id: uuid.UUID, db: Session = Depends(get_db)):
    return booking_service.get_bookings_by_parent_id(db=db, parent_id=parent_id)

@router.put('/{booking_id}', response_model=booking_model.Booking)
def update_booking(booking_id: uuid.UUID, booking: booking_model.BookingUpdate, db: Session = Depends(get_db)):
    try:
        return booking_service.update_booking(db=db, booking_id=booking_id, booking_data=booking)
    except HTTPException as e:
        raise e
