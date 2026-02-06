import uuid

from django.http import JsonResponse
from fastapi.responses import JSONResponse

from config.error_exception import ExceptionError
from config.response import APIResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import logging
from . import payment_model, payment_service
from .response import LegacyPaymentProcessor
from modules.booking.booking_service import update_booking, get_booking_details
from modules.booking.booking_model import BookingUpdate
from config.database import get_db
from config.rate_limiting import limiter

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

payment_processor = LegacyPaymentProcessor()


@router.post(
    "/process",
    response_model=APIResponse[payment_model.TransactionResponse],
    responses={
        400: {"model": APIResponse[None]},
        422: {"model": APIResponse[None]},
        500: {"model": APIResponse[None]},
    },
)
@limiter.limit("20/minute")  # Limit to 5 payment attempts per minute per IP
def process_payment(
    payment_data: payment_model.PaymentRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        booking_id = uuid.UUID(payment_data.activity_id)
        booking = get_booking_details(db, booking_id)

        if booking.status == "paid":
            raise ExceptionError(
                "This booking has already been paid for", status_code=422
            )

        payment_response = payment_processor.process_payment(payment_data.model_dump())

        payment_service.create_payment_record(db, booking_id, payment_response)

        if not payment_response.success:
            raise ExceptionError(payment_response.error_message, status_code=400)

        update_booking(db, booking_id, BookingUpdate(status="paid"))
        return APIResponse(
            status="success",
            data=payment_model.TransactionResponse(
                transaction_id=payment_response.transaction_id
            ),
            error=None,
        )
    except ExceptionError as e:
        logging.error(f"Payment failed booking {booking_id}: {str(e)}")
        # If booking update fails, we have a problem.
        # In a real-world scenario, you'd want to handle this gracefully.
        # For example, by logging the error and notifying an admin.
        # For now, we'll return an error to the user.
        # i modifed this reponse because the format of the data.
        # return payment_model.PaymentResponse(
        #     success=False,
        #     error_message=f"Payment succeeded but failed to update booking: {str(e)}"
        # )
        return JSONResponse(
            status_code=e.status_code if hasattr(e, "status_code") else 500,
            content=APIResponse(
                status="error",
                data=None,
                error=f"Payment failed - {str(e)}",
            ).model_dump(),
        )
