from enum import Enum
from dataclasses import dataclass

class LeadStatus(str, Enum):
    NEW="NEW"; QUALIFIED="QUALIFIED"; CONTACTED="CONTACTED"; DELIVERED="DELIVERED"; REPLIED="REPLIED"; INTERESTED="INTERESTED"; PAYMENT_PENDING="PAYMENT_PENDING"; PAID="PAID"; FULFILLMENT="FULFILLMENT"; COMPLETED="COMPLETED"; LOST="LOST"; OPTED_OUT="OPTED_OUT"

class PaymentStatus(str, Enum):
    CREATED="CREATED"; PAYMENT_PENDING="PAYMENT_PENDING"; PAYMENT_DETECTED="PAYMENT_DETECTED"; PAYMENT_VERIFIED="PAYMENT_VERIFIED"; PAID="PAID"; FAILED="FAILED"; CANCELLED="CANCELLED"; REFUNDED="REFUNDED"

@dataclass(frozen=True)
class Package:
    code: str
    name: str
    price_inr: int

PACKAGES = {
    "digital_identity": Package("digital_identity", "Digital Identity", 4999),
    "growth_suite": Package("growth_suite", "Growth Suite", 12999),
}

FORBIDDEN_AI_ACTIONS = frozenset({"verify_payment","modify_financial_record","issue_refund","bypass_opt_out","change_security_settings","access_secret"})
