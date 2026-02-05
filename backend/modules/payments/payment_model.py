from pydantic import BaseModel, Field
from typing import Optional

class PaymentRequest(BaseModel):
    student_name: str
    parent_name: str
    amount: float = Field(gt=0, description="Payment amount must be a positive number.")
    card_number: str = Field(..., min_length=16, max_length=16, pattern="^[0-9]{16}$")
    expiry_date: str = Field(..., pattern="^(0[1-9]|1[0-2])\\/?([0-9]{2})$")
    cvv: str = Field(..., min_length=3, max_length=3, pattern="^[0-9]{3}$")
    school_id: str
    activity_id: str # This is the booking_id

class PaymentResponse(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None
