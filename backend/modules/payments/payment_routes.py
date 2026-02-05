import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from config import logging
from . import payment_model, payment_service
from .response import LegacyPaymentProcessor
from modules.booking.booking_service import update_booking, get_booking_details
from modules.booking.booking_model import BookingUpdate
from config.database import get_db
from middlewares.response_middleware import UniformRoute
from config.rate_limiting import limiter

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    route_class=UniformRoute
)

payment_processor = LegacyPaymentProcessor()

@router.post('/process')
@limiter.limit("5/minute")  # Limit to 5 payment attempts per minute per IP
def process_payment(payment_data: payment_model.PaymentRequest, request: Request, db: Session = Depends(get_db)):
    
    booking_id = uuid.UUID(payment_data.activity_id)
    booking = get_booking_details(db, booking_id)

    if booking.status == 'paid':
        raise HTTPException(status_code=400, detail="This booking has already been paid for.")

    payment_response = payment_processor.process_payment(payment_data.dict())
    
    payment_service.create_payment_record(db, booking_id, payment_response)

    if not payment_response.success:
        logging.info(f"Payment succeeded {booking_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=payment_response.error_message)

    try:
        update_booking(db, booking_id, BookingUpdate(status='paid'))
        return payment_response.transaction_id;
    except (ValueError, HTTPException) as e:
         logging.error(f"Payment succeeded but failed to update booking {booking_id}: {str(e)}")
            # If booking update fails, we have a problem.
            # In a real-world scenario, you'd want to handle this gracefully.
            # For example, by logging the error and notifying an admin.
            # For now, we'll return an error to the user.
            # i modifed this reponse because the format of the data.
            # return payment_model.PaymentResponse(
            #     success=False,
            #     error_message=f"Payment succeeded but failed to update booking: {str(e)}"
            # )
         raise HTTPException(status_code=500, detail=f"Payment succeeded but failed to update booking: {str(e)}")

