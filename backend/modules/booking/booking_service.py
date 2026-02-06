from sqlalchemy.orm import Session
from fastapi import HTTPException

from config.error_exception import ExceptionError
from . import booking_schema, booking_model
from modules.trips.trip_schema import Trip
from modules.parents.parent_schema import Parent
from modules.students.student_schema import Student
import uuid


def get_or_create_booking(
    db: Session, booking: booking_model.BookingCreate
) -> booking_model.BookingDetails:
    existing_booking = (
        db.query(booking_schema.Booking)
        .filter(
            booking_schema.Booking.trip_id == booking.trip_id,
            booking_schema.Booking.parent_id == booking.parent_id,
            booking_schema.Booking.student_id == booking.student_id,
        )
        .first()
    )

    if existing_booking:
        return get_booking_details(db, existing_booking.id)

    # Validate foreign keys
    trip = db.query(Trip).filter(Trip.id == booking.trip_id).first()
    if not trip:
        raise ExceptionError("Trip not found", status_code=404)
    if not db.query(Parent).filter(Parent.id == booking.parent_id).first():
        raise ExceptionError("Parent not found", status_code=404)
    if not db.query(Student).filter(Student.id == booking.student_id).first():
        raise ExceptionError("Student not found", status_code=404)
    new_booking_data = booking.model_dump()

    # Calculate total price based on trip price, assuming no discounts or additional fees for simplicity
    new_booking_data["total_in_cents"] = trip.price_in_cents

    # Set initial status to 'pending'
    new_booking_data["status"] = "pending"

    new_booking = booking_schema.Booking(**new_booking_data)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return get_booking_details(db, new_booking.id)


def _get_booking_by_id(db: Session, booking_id: uuid.UUID) -> booking_schema.Booking:
    booking = (
        db.query(booking_schema.Booking)
        .filter(booking_schema.Booking.id == booking_id)
        .first()
    )
    if not booking:
        raise ExceptionError("Booking not found", status_code=404)
    return booking


def get_booking_details(
    db: Session, booking_id: uuid.UUID
) -> booking_model.BookingDetails:
    booking_details = (
        db.query(
            booking_schema.Booking,
            Student.name.label("student_name"),
            Trip.name.label("trip_name"),
            Trip.school_id,
        )
        .join(Student, booking_schema.Booking.student_id == Student.id)
        .join(Trip, booking_schema.Booking.trip_id == Trip.id)
        .filter(booking_schema.Booking.id == booking_id)
        .first()
    )

    if not booking_details:
        raise ExceptionError("Booking not found", status_code=404)

    booking, student_name, trip_name, school_id = booking_details

    return booking_model.BookingDetails(
        id=booking.id,
        description=booking.description,
        trip_name=trip_name,
        parent_id=booking.parent_id,
        student_name=student_name,
        school_id=school_id,
        total_in_cents=booking.total_in_cents,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )


def get_bookings_by_parent_id(
    db: Session, parent_id: uuid.UUID
) -> list[booking_model.BookingDetails]:
    bookings_details = (
        db.query(
            booking_schema.Booking,
            Student.name.label("student_name"),
            Trip.name.label("trip_name"),
            Trip.school_id,
        )
        .join(Student, booking_schema.Booking.student_id == Student.id)
        .join(Trip, booking_schema.Booking.trip_id == Trip.id)
        .filter(booking_schema.Booking.parent_id == parent_id)
        .all()
    )

    return [
        booking_model.BookingDetails(
            id=booking.id,
            description=booking.description,
            trip_name=trip_name,
            school_id=school_id,
            parent_id=booking.parent_id,
            student_name=student_name,
            total_in_cents=booking.total_in_cents,
            status=booking.status,
            created_at=booking.created_at,
            updated_at=booking.updated_at,
        )
        for booking, student_name, trip_name, school_id in bookings_details
    ]


def update_booking(
    db: Session, booking_id: uuid.UUID, booking_data: booking_model.BookingUpdate
) -> booking_schema.Booking:
    booking = _get_booking_by_id(db, booking_id)

    for key, value in booking_data.model_dump(exclude_unset=True).items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking
