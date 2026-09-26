from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

def now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str]=mapped_column(String(128))
    role: Mapped[str]=mapped_column(String(40), default="ADMIN")
    active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)

class Business(Base):
    __tablename__="businesses"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(255), index=True)
    locality: Mapped[str|None]=mapped_column(String(255))
    city: Mapped[str]=mapped_column(String(120), default="Amravati")
    state: Mapped[str]=mapped_column(String(120), default="Maharashtra")
    phone: Mapped[str|None]=mapped_column(String(40), index=True)
    email: Mapped[str|None]=mapped_column(String(320))
    website: Mapped[str|None]=mapped_column(String(500))
    sector: Mapped[str|None]=mapped_column(String(120))
    source: Mapped[str|None]=mapped_column(String(120))
    source_url: Mapped[str|None]=mapped_column(String(500))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    leads=relationship("Lead", back_populates="business", cascade="all, delete-orphan")

class Lead(Base):
    __tablename__="leads"
    __table_args__=(UniqueConstraint("business_id","email","phone", name="uq_lead_contact"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    business_id: Mapped[int]=mapped_column(ForeignKey("businesses.id"), index=True)
    package: Mapped[str|None]=mapped_column(String(80))
    status: Mapped[str]=mapped_column(String(40), default="NEW", index=True)
    lead_score: Mapped[int]=mapped_column(Integer, default=0)
    digital_presence_score: Mapped[int]=mapped_column(Integer, default=0)
    opted_out: Mapped[bool]=mapped_column(Boolean, default=False, index=True)
    notes: Mapped[str|None]=mapped_column(Text)
    last_contacted_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    last_replied_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    business=relationship("Business", back_populates="leads")

class Order(Base):
    __tablename__="orders"
    id: Mapped[int]=mapped_column(primary_key=True)
    lead_id: Mapped[int|None]=mapped_column(ForeignKey("leads.id"), index=True)
    business_id: Mapped[int]=mapped_column(ForeignKey("businesses.id"), index=True)
    package: Mapped[str]=mapped_column(String(80))
    amount: Mapped[Decimal]=mapped_column(Numeric(12,2))
    status: Mapped[str]=mapped_column(String(40), default="PAYMENT_PENDING", index=True)
    currency: Mapped[str]=mapped_column(String(8), default="INR")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now, onupdate=now)

class Payment(Base):
    __tablename__="payments"
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey("orders.id"), index=True)
    amount: Mapped[Decimal]=mapped_column(Numeric(12,2))
    transaction_ref: Mapped[str|None]=mapped_column(String(255), unique=True)
    status: Mapped[str]=mapped_column(String(40), default="CREATED", index=True)
    provider: Mapped[str|None]=mapped_column(String(80))
    verified_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)

class Invoice(Base):
    __tablename__="invoices"
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey("orders.id"), unique=True)
    invoice_number: Mapped[str]=mapped_column(String(80), unique=True)
    total: Mapped[Decimal]=mapped_column(Numeric(12,2))
    status: Mapped[str]=mapped_column(String(30), default="ISSUED")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)

class AuditLog(Base):
    __tablename__="audit_logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    actor: Mapped[str]=mapped_column(String(255))
    action: Mapped[str]=mapped_column(String(120), index=True)
    entity_type: Mapped[str|None]=mapped_column(String(80))
    entity_id: Mapped[str|None]=mapped_column(String(80))
    detail: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
