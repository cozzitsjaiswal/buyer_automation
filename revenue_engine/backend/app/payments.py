from urllib.parse import urlencode
from .config import settings

def build_upi_url(amount_inr: int, order_id: str) -> str:
    if not settings.upi_vpa or not settings.upi_payee_name:
        raise ValueError("UPI_VPA and UPI_PAYEE_NAME must be configured")
    params = {"pa": settings.upi_vpa, "pn": settings.upi_payee_name, "am": f"{amount_inr:.2f}", "cu": "INR", "tn": f"Order {order_id}"}
    return "upi://pay?" + urlencode(params)

def verify_payment(expected_amount: int, received_amount: int, transaction_id: str, already_seen: bool=False) -> dict:
    if already_seen: raise ValueError("Duplicate transaction reference")
    if expected_amount != received_amount: raise ValueError("Payment amount mismatch")
    if not transaction_id.strip(): raise ValueError("Transaction reference required")
    return {"verified": True, "transaction_id": transaction_id, "amount": received_amount}
