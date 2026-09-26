from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from .db import get_db
from .models import AuditLog, Business, Invoice, Lead, Order, Payment, User
from .schemas import LeadIn, LeadOut, LoginIn, OrderIn, PaymentVerifyIn, TokenOut
from .security import create_token, hash_password, verify_password
from .dependencies import current_user

router=APIRouter(prefix="/api")

PACKAGES={"digital_identity":Decimal("4999"),"growth_suite":Decimal("12999")}
from decimal import Decimal

def audit(db, actor, action, typ=None, entity_id=None, detail=None):
    db.add(AuditLog(actor=actor,action=action,entity_type=typ,entity_id=str(entity_id) if entity_id else None,detail=detail))
    db.commit()

@router.post("/auth/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==data.email).first()
    if not user or not user.active or not verify_password(data.password,user.password_hash):
        raise HTTPException(401,"Invalid credentials")
    return TokenOut(access_token=create_token(user.email,user.role))

@router.post("/auth/bootstrap",response_model=TokenOut)
def bootstrap(data:LoginIn,db:Session=Depends(get_db)):
    if db.query(User).count(): raise HTTPException(409,"Admin already exists")
    user=User(email=data.email,password_hash=hash_password(data.password),role="SUPER_ADMIN")
    db.add(user); db.commit()
    return TokenOut(access_token=create_token(user.email,user.role))

@router.get("/leads",response_model=list[LeadOut])
def leads(status:str|None=None,limit:int=Query(50,le=200),offset:int=0,db:Session=Depends(get_db),user=Depends(current_user)):
    q=db.query(Lead)
    if status: q=q.filter(Lead.status==status)
    return q.order_by(Lead.created_at.desc()).offset(offset).limit(limit).all()

@router.post("/leads",response_model=LeadOut)
def create_lead(data:LeadIn,db:Session=Depends(get_db),user=Depends(current_user)):
    b=Business(name=data.business_name,locality=data.locality,phone=data.phone,email=data.email,sector=data.sector,website=data.website,source=data.source,source_url=data.source_url)
    db.add(b); db.flush()
    score=20 + (20 if data.website else 0) + (15 if data.email else 0) + (10 if data.phone else 0)
    l=Lead(business_id=b.id,package=data.package,status="NEW",lead_score=min(score,100),digital_presence_score=40 if data.website else 15,notes=data.notes)
    db.add(l); db.commit(); db.refresh(l)
    audit(db,user.email,"LEAD_CREATED","lead",l.id,data.business_name)
    return l

@router.post("/leads/{lead_id}/opt-out")
def opt_out(lead_id:int,db:Session=Depends(get_db),user=Depends(current_user)):
    l=db.get(Lead,lead_id)
    if not l: raise HTTPException(404,"Lead not found")
    l.opted_out=True; l.status="OPTED_OUT"; db.commit(); audit(db,user.email,"LEAD_OPTED_OUT","lead",lead_id)
    return {"status":"ok"}

@router.post("/orders")
def create_order(data:OrderIn,db:Session=Depends(get_db),user=Depends(current_user)):
    l=db.get(Lead,data.lead_id)
    if not l: raise HTTPException(404,"Lead not found")
    if l.opted_out: raise HTTPException(409,"Lead opted out")
    amount=PACKAGES.get(data.package)
    if amount is None: raise HTTPException(400,"Unknown package")
    o=Order(lead_id=l.id,business_id=l.business_id,package=data.package,amount=amount)
    db.add(o); db.flush()
    db.add(Payment(order_id=o.id,amount=amount,status="PAYMENT_PENDING"))
    l.status="PAYMENT_PENDING"; db.commit(); db.refresh(o)
    audit(db,user.email,"ORDER_CREATED","order",o.id,data.package)
    return {"id":o.id,"package":o.package,"amount":str(o.amount),"status":o.status}

@router.post("/orders/{order_id}/verify")
def verify(order_id:int,data:PaymentVerifyIn,db:Session=Depends(get_db),user=Depends(current_user)):
    o=db.get(Order,order_id)
    if not o: raise HTTPException(404,"Order not found")
    if data.amount != o.amount: raise HTTPException(409,"Payment amount mismatch")
    existing=db.query(Payment).filter(Payment.transaction_ref==data.transaction_ref).first()
    if existing: raise HTTPException(409,"Duplicate transaction reference")
    p=db.query(Payment).filter(Payment.order_id==o.id).first()
    p.transaction_ref=data.transaction_ref; p.provider=data.provider; p.status="PAYMENT_VERIFIED"; p.verified_at=datetime.now(timezone.utc)
    o.status="PAID"; l=db.get(Lead,o.lead_id) if o.lead_id else None
    if l: l.status="FULFILLMENT"
    db.commit(); audit(db,user.email,"PAYMENT_VERIFIED","order",o.id,data.transaction_ref)
    return {"status":"PAID","order_id":o.id}

@router.get("/dashboard/metrics")
def metrics(db:Session=Depends(get_db),user=Depends(current_user)):
    counts={s:db.query(func.count(Lead.id)).filter(Lead.status==s).scalar() for s in ["NEW","QUALIFIED","CONTACTED","REPLIED","INTERESTED","PAYMENT_PENDING","PAID","FULFILLMENT","COMPLETED","OPTED_OUT"]}
    revenue=db.query(func.coalesce(func.sum(Order.amount),0)).filter(Order.status=="PAID").scalar()
    return {"leads":db.query(func.count(Lead.id)).scalar(),"revenue":float(revenue or 0),**{k.lower():v for k,v in counts.items()}}

@router.get("/audit-logs")
def audit_logs(limit:int=100,db:Session=Depends(get_db),user=Depends(current_user)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(min(limit,500)).all()
