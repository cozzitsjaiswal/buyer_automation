from app.domain import PACKAGES, LeadStatus
from app.payments import verify_payment

def test_packages():
    assert PACKAGES["digital_identity"].price_inr == 4999
    assert PACKAGES["growth_suite"].price_inr == 12999

def test_payment_verification():
    assert verify_payment(4999,4999,"TX123")["verified"] is True

def test_lead_status():
    assert LeadStatus.OPTED_OUT.value == "OPTED_OUT"
