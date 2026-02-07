from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Text

from database import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    country = Column(String(120), nullable=False, index=True)
    city = Column(String(120), nullable=True)
    buyer_type = Column(String(50), nullable=False)
    contact_person = Column(String(255), nullable=True)
    designation = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(80), nullable=True)
    website = Column(String(255), nullable=True)
    source = Column(String(50), nullable=False)
    product_interest = Column(String(50), nullable=False)
    moq = Column(String(120), nullable=True)
    price_discussed = Column(Float, nullable=True)
    payment_terms = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="New", index=True)
    last_contact_date = Column(Date, nullable=True)
    next_follow_up_date = Column(Date, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class BuyerBase(BaseModel):
    company_name: str
    country: str
    city: Optional[str] = None
    buyer_type: str
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    source: str
    product_interest: str
    moq: Optional[str] = None
    price_discussed: Optional[float] = None
    payment_terms: Optional[str] = None
    status: str = "New"
    last_contact_date: Optional[date] = None
    next_follow_up_date: Optional[date] = None
    remarks: Optional[str] = None

    @field_validator("buyer_type")
    @classmethod
    def validate_buyer_type(cls, value: str) -> str:
        allowed = {"Importer", "Wholesaler", "Processor"}
        if value not in allowed:
            raise ValueError(f"buyer_type must be one of: {', '.join(sorted(allowed))}")
        return value

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        allowed = {"Google Maps", "B2B", "LinkedIn", "Manual"}
        if value not in allowed:
            raise ValueError(f"source must be one of: {', '.join(sorted(allowed))}")
        return value

    @field_validator("product_interest")
    @classmethod
    def validate_product_interest(cls, value: str) -> str:
        allowed = {"Turmeric", "Dal", "Multiple"}
        if value not in allowed:
            raise ValueError(f"product_interest must be one of: {', '.join(sorted(allowed))}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        allowed = {"New", "Contacted", "Sample Sent", "Negotiation", "Closed", "Lost"}
        if value not in allowed:
            raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
        return value


class BuyerCreate(BuyerBase):
    pass


class BuyerUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"New", "Contacted", "Sample Sent", "Negotiation", "Closed", "Lost"}
        if value not in allowed:
            raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
        return value


class BuyerResponse(BuyerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
