from pydantic import BaseModel, Field
from typing import Optional


class PaymentRequest(BaseModel):
    student_name: str
    parent_name: str
    amount: float
    card_number: str
    expiry_date: str
    cvv: str
    school_id: str
    activity_id: str  # This is the booking_id


class PaymentResponse(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None


class TransactionResponse(BaseModel):
    transaction_id: str
