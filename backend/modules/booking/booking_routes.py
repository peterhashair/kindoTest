import logging
from config.response import APIResponse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uuid
from config.database import get_db
from . import booking_model, booking_service

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "/",
    response_model=APIResponse[booking_model.BookingDetails],
    responses={422: {"model": APIResponse[None]}},
)
def get_or_create_booking(
    booking: booking_model.BookingCreate, db: Session = Depends(get_db)
):
    try:
        book = booking_service.get_or_create_booking(db=db, booking=booking)
        return APIResponse(status="success", data=book, error="")
    except Exception as e:
        logging.error(f"Error creating or fetching booking: {str(e)}")
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )


@router.get(
    "/{booking_id}",
    response_model=APIResponse[booking_model.BookingDetails],
    responses={422: {"model": APIResponse[None]}},
)
def get_booking(booking_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        booking_details = booking_service.get_booking_details(
            db=db, booking_id=booking_id
        )
        return APIResponse(status="success", data=booking_details, error="")
    except Exception as e:
        logging.error(f"Error fetching booking {booking_id}: {str(e)}")
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )


@router.get(
    "/parent/{parent_id}",
    response_model=APIResponse[list[booking_model.BookingDetails]],
    responses={422: {"model": APIResponse[None]}},
)
def get_bookings_by_parent(parent_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        bookings = booking_service.get_bookings_by_parent_id(db=db, parent_id=parent_id)
        return APIResponse(status="success", data=bookings, error="")
    except Exception as e:
        logging.error(f"Error fetching bookings for parent {parent_id}: {str(e)}")
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )


@router.put(
    "/{booking_id}",
    response_model=APIResponse[booking_model.Booking],
    responses={422: {"model": APIResponse[None]}},
)
def update_booking(
    booking_id: uuid.UUID,
    booking: booking_model.BookingUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_booking = booking_service.update_booking(
            db=db, booking_id=booking_id, booking_data=booking
        )
        return APIResponse(status="success", data=updated_booking, error="")
    except Exception as e:
        logging.error(f"Error updating booking {booking_id}: {str(e)}")
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(status="error", data=None, error=str(e)).model_dump(),
        )
