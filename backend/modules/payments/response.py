import time
import random
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class PaymentResponse:
    """
    Represents the response from a payment processing operation.
    """
    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None

class LegacyPaymentProcessor:
    """
    A legacy payment processor that accepts payments and provides responses.
    This is a simulation of an external API you'd need to work with.
    """

    def process_payment(self, payment_data: Dict[str, Any]) -> PaymentResponse:
        """
        Process a payment with the following required fields:
        - student_name: str
        - parent_name: str
        - amount: float
        - card_number: str (must be 16 digits)
        - expiry_date: str (format: MM/YY)
        - cvv: str (must be 3 digits)
        - school_id: str
        - activity_id: str
        """
        required_fields = [
            'student_name', 'parent_name', 'amount', 'card_number', 
            'expiry_date', 'cvv', 'school_id', 'activity_id'
        ]

        # Validate all required fields exist
        for field in required_fields:
            if field not in payment_data:
                return PaymentResponse(
                    success=False,
                    error_message=f"Missing required field: {field}"
                )

        # Validate card number (must be 16 digits)
        card_num = str(payment_data.get('card_number', '')).replace(' ', '')
        if not (card_num.isdigit() and len(card_num) == 16):
            return PaymentResponse(
                success=False,
                error_message="Invalid card number. Must be 16 digits."
            )

        # Validate expiry date format (MM/YY)
        if not self._validate_expiry_format(str(payment_data.get('expiry_date', ''))):
            return PaymentResponse(
                success=False,
                error_message="Invalid expiry date format. Must be MM/YY."
            )

        # Validate expiry date is in the future
        if not self._validate_expiry_date(str(payment_data.get('expiry_date', ''))):
            return PaymentResponse(
                success=False,
                error_message="Card has expired. Please use a valid card."
            )
            
        # Validate CVV (must be 3 digits)
        cvv = str(payment_data.get('cvv', ''))
        if not (cvv.isdigit() and len(cvv) == 3):
            return PaymentResponse(
                success=False,
                error_message="Invalid CVV. Must be 3 digits."
            )

        # Validate amount is positive
        amount = payment_data.get('amount', 0)
        if not isinstance(amount, (int, float)) or amount <= 0:
            return PaymentResponse(
                success=False,
                error_message="Payment amount must be a positive number."
            )

        # Simulate processing time
        time.sleep(1.5)

        # Simulate occasional payment failures
        if random.random() < 0.1:  # 10% chance of failure
            return PaymentResponse(
                success=False,
                error_message="Payment declined by processor. Please try again."
            )

        # Generate a transaction ID for successful payments
        transaction_id = f"TX-{int(time.time())}-{random.randint(1000, 9999)}"
        return PaymentResponse(
            success=True,
            transaction_id=transaction_id
        )

    def _validate_expiry_format(self, expiry: str) -> bool:
        """Validate the expiry date is in MM/YY format."""
        if len(expiry) != 5 or expiry[2] != '/':
            return False
        
        parts = expiry.split('/')
        if len(parts) != 2:
            return False
            
        month, year = parts
        if not (month.isdigit() and year.isdigit()):
            return False
            
        month_num = int(month)
        return 1 <= month_num <= 12

    def _validate_expiry_date(self, expiry: str) -> bool:
        """this is the new function i added to Validate the expiry date is in the future."""
        from datetime import datetime
        try:
            exp_month, exp_year = map(int, expiry.split('/'))
            exp_year += 2000  # Convert YY to YYYY
            now = datetime.now()
            return (exp_year > now.year) or (exp_year == now.year and exp_month >= now.month)
        except ValueError:
            return False