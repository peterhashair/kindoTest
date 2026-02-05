from sqlalchemy.orm import Session
from . import payment_schema, payment_model
from modules.booking.booking_schema import Booking
import uuid

def create_payment_record(db: Session, booking_id: uuid.UUID, payment_response: payment_model.PaymentResponse):
    
    payment_status = "success" if payment_response.success else "failed"

    new_payment = payment_schema.Payment(
        booking_id=booking_id,
        status=payment_status,
        transaction_id=payment_response.transaction_id,
        error_message=payment_response.error_message
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment
