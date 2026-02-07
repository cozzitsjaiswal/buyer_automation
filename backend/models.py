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
        """
        Ensure the provided buyer_type is one of the allowed values: 'Importer', 'Wholesaler', or 'Processor'.
        
        Parameters:
            value (str): The buyer type to validate.
        
        Returns:
            str: The original `value` if it is valid.
        
        Raises:
            ValueError: If `value` is not one of the allowed buyer types.
        """
        allowed = {"Importer", "Wholesaler", "Processor"}
        if value not in allowed:
            raise ValueError(f"buyer_type must be one of: {', '.join(sorted(allowed))}")
        return value

    @field_validator("source")
    @classmethod
    def validate_source(cls, value: str) -> str:
        """
        Validate that `value` is one of the allowed buyer source options.
        
        Parameters:
            value (str): Source identifier to validate. Allowed values: "Google Maps", "B2B", "LinkedIn", "Manual".
        
        Returns:
            str: The validated source string.
        
        Raises:
            ValueError: If `value` is not one of the allowed options.
        """
        allowed = {"Google Maps", "B2B", "LinkedIn", "Manual"}
        if value not in allowed:
            raise ValueError(f"source must be one of: {', '.join(sorted(allowed))}")
        return value

    @field_validator("product_interest")
    @classmethod
    def validate_product_interest(cls, value: str) -> str:
        """
        Validate that product_interest is one of "Turmeric", "Dal", or "Multiple".
        
        Parameters:
            value (str): Candidate product interest.
        
        Returns:
            str: The validated value.
        
        Raises:
            ValueError: If value is not one of "Turmeric", "Dal", "Multiple".
        """
        allowed = {"Turmeric", "Dal", "Multiple"}
        if value not in allowed:
            raise ValueError(f"product_interest must be one of: {', '.join(sorted(allowed))}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        """
        Validate that `value` is one of the allowed buyer status strings.
        
        Parameters:
            cls: The class where the validator is defined.
            value (str): Candidate status string to validate.
        
        Returns:
            str: The validated status string.
        
        Raises:
            ValueError: If `value` is not one of "New", "Contacted", "Sample Sent", "Negotiation", "Closed", or "Lost".
        """
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
        """
        Validate that a buyer status is either None or one of the allowed status values.
        
        Parameters:
            value (Optional[str]): The status value to validate.
        
        Returns:
            Optional[str]: The validated status value (unchanged) when valid, or None.
        
        Raises:
            ValueError: If `value` is not None and is not one of: Closed, Contacted, Lost, New, Negotiation, Sample Sent.
        """
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