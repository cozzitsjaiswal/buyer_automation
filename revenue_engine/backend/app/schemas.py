from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class LeadIn(BaseModel):
    business_name: str = Field(min_length=2, max_length=255)
    locality: str|None=None
    phone: str|None=None
    email: EmailStr|None=None
    sector: str|None=None
    package: str|None=None
    website: str|None=None
    source: str|None=None
    source_url: str|None=None
    notes: str|None=None

class LeadOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    business_id:int
    package:str|None
    status:str
    lead_score:int
    digital_presence_score:int
    opted_out:bool

class OrderIn(BaseModel):
    lead_id:int
    package:str

class PaymentVerifyIn(BaseModel):
    transaction_ref:str = Field(min_length=3)
    amount:Decimal
    provider:str="manual"

class TokenOut(BaseModel):
    access_token:str
    token_type:str="bearer"
