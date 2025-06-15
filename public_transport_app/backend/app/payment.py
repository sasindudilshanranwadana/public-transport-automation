# backend/app/payment.py
import os

def process_payment(trip_id: str, amount: float, token: str = None) -> dict:
    """
    Simulated free payment for student project.
    Always returns success with a dummy receipt_id.
    """
    # amount and token are ignored
    return {"success": True, "receipt_id": f"FREE-{trip_id}"}
