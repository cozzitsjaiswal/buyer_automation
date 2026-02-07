from datetime import datetime
from io import BytesIO
from typing import List, Optional

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Buyer, BuyerCreate, BuyerResponse, BuyerUpdate
from scraper import scrape_company_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EU Buyer Automation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLsPayload(BaseModel):
    urls: List[str]
    country: str = "Unknown"
    city: Optional[str] = None
    buyer_type: str = "Importer"
    source: str = "Manual"
    product_interest: str = "Turmeric"


@app.get("/health")
def health_check():
    """
    Provide a simple health status for the service.
    
    Returns:
        dict: Keys:
            status (str): "ok" when the service is healthy.
            service (str): The service name "EU Buyer Automation System".
    """
    return {"status": "ok", "service": "EU Buyer Automation System"}


@app.post("/buyers", response_model=BuyerResponse)
def create_buyer(payload: BuyerCreate, db: Session = Depends(get_db)):
    """
    Create a new Buyer record from the provided payload and persist it to the database.
    
    Parameters:
        payload (BuyerCreate): Data used to populate the new Buyer record.
    
    Returns:
        Buyer: The persisted Buyer instance with database-generated fields (for example `id` and timestamps) populated.
    """
    buyer = Buyer(**payload.model_dump())
    db.add(buyer)
    db.commit()
    db.refresh(buyer)
    return buyer


@app.get("/buyers", response_model=List[BuyerResponse])
def get_buyers(
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Retrieve buyers filtered by an optional search term and/or status, ordered by creation date descending.
    
    Parameters:
        search (Optional[str]): Substring to match against company_name or country (case-insensitive).
        status (Optional[str]): Exact status value to filter by.
        limit (int): Maximum number of buyers to return (between 1 and 1000).
    
    Returns:
        List[Buyer]: Buyers matching the filters, ordered by created_at descending and limited to `limit`.
    """
    query = db.query(Buyer)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Buyer.company_name.ilike(pattern), Buyer.country.ilike(pattern)))
    if status:
        query = query.filter(Buyer.status == status)

    return query.order_by(desc(Buyer.created_at)).limit(limit).all()


@app.get("/buyers/{buyer_id}", response_model=BuyerResponse)
def get_buyer(buyer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a Buyer by its primary key.
    
    Parameters:
        buyer_id (int): Primary key of the buyer to retrieve.
    
    Returns:
        Buyer: The Buyer database model instance.
    
    Raises:
        HTTPException: If no Buyer exists with the given id (404).
    """
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer


@app.patch("/buyers/{buyer_id}", response_model=BuyerResponse)
def update_buyer(buyer_id: int, payload: BuyerUpdate, db: Session = Depends(get_db)):
    """
    Update fields of an existing Buyer record and refresh its last contact date.
    
    Only fields present in `payload` are applied to the Buyer; when any field is updated,
    `last_contact_date` is set to the current UTC date.
    
    Parameters:
    	buyer_id (int): ID of the Buyer to update.
    	payload (BuyerUpdate): Partial update payload; only supplied fields are written.
    	db (Session, optional): Database session dependency (omitted from docs where injected).
    
    Returns:
    	Buyer: The updated Buyer instance.
    
    Raises:
    	HTTPException: 404 if no Buyer with `buyer_id` exists.
    """
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(buyer, key, value)

    if update_data:
        buyer.last_contact_date = datetime.utcnow().date()

    db.commit()
    db.refresh(buyer)
    return buyer


@app.delete("/buyers/{buyer_id}")
def delete_buyer(buyer_id: int, db: Session = Depends(get_db)):
    """
    Delete a buyer record by its ID.
    
    Parameters:
        buyer_id (int): ID of the buyer to delete.
    
    Raises:
        HTTPException: with status 404 if no buyer with the given ID exists.
    
    Returns:
        dict: {"message": "Buyer deleted"} on successful deletion.
    """
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    db.delete(buyer)
    db.commit()
    return {"message": "Buyer deleted"}


@app.get("/dashboard")
def dashboard_summary(db: Session = Depends(get_db)):
    """
    Produce a dashboard summary of buyers including total count, counts by status, and the 10 most recent buyers.
    
    Returns:
        dict: {
            "total_buyers": int,                     # total number of buyers
            "status_cards": List[dict],              # each dict has keys "status" (str) and "count" (int)
            "latest_buyers": List[Buyer]             # up to 10 Buyer instances ordered by created_at descending
        }
    """
    total_buyers = db.query(func.count(Buyer.id)).scalar()
    by_status = (
        db.query(Buyer.status, func.count(Buyer.id).label("count"))
        .group_by(Buyer.status)
        .order_by(Buyer.status)
        .all()
    )
    latest = db.query(Buyer).order_by(desc(Buyer.created_at)).limit(10).all()
    return {
        "total_buyers": total_buyers,
        "status_cards": [{"status": row.status, "count": row.count} for row in by_status],
        "latest_buyers": latest,
    }


@app.post("/import-urls")
def import_urls(payload: URLsPayload, db: Session = Depends(get_db)):
    """
    Import a list of company URLs by scraping each and creating Buyer records in the database.
    
    Processes each non-empty URL from payload.urls, scrapes company data, creates and persists a Buyer using scraped values (falls back to "Unknown Company" for missing company name) and metadata from the payload, and records per-URL outcomes. For each URL the result includes the URL, a boolean `success`, and either `buyer_id` on success or an `error` message on failure. Empty or whitespace-only URLs are skipped.
    
    Parameters:
        payload (URLsPayload): Payload containing `urls` and default metadata fields (country, city, buyer_type, source, product_interest).
    
    Returns:
        dict: {"results": list} where each list item is a dict with keys:
            - "url" (str): the processed URL
            - "success" (bool): `true` if the buyer was created, `false` otherwise
            - "buyer_id" (int, optional): ID of the created Buyer when successful
            - "error" (str, optional): error message when creation failed
    """
    results = []
    for raw_url in payload.urls:
        url = raw_url.strip()
        if not url:
            continue

        try:
            extracted = scrape_company_data(url)
            buyer = Buyer(
                company_name=extracted.get("company_name") or "Unknown Company",
                country=payload.country,
                city=payload.city,
                buyer_type=payload.buyer_type,
                contact_person=None,
                designation=None,
                email=extracted.get("email"),
                phone=extracted.get("phone"),
                website=extracted.get("website"),
                source=payload.source,
                product_interest=payload.product_interest,
                moq=None,
                price_discussed=None,
                payment_terms=None,
                status="New",
                remarks="Imported from URL scrape",
            )
            db.add(buyer)
            db.commit()
            db.refresh(buyer)
            results.append({"url": url, "success": True, "buyer_id": buyer.id})
        except Exception as exc:
            db.rollback()
            results.append({"url": url, "success": False, "error": str(exc)})

    return {"results": results}


@app.get("/export")
def export_buyers(db: Session = Depends(get_db)):
    """
    Create an Excel (.xlsx) file containing all buyers ordered by creation date.
    
    The spreadsheet includes one row per buyer with columns: id, company_name, country, city, buyer_type, contact_person, designation, email, phone, website, source, product_interest, moq, price_discussed, payment_terms, status, last_contact_date, next_follow_up_date, remarks, and created_at.
    
    Returns:
        StreamingResponse: A response whose body is the Excel file and which sets the filename to "EU_Turmeric_Buyers.xlsx".
    """
    buyers = db.query(Buyer).order_by(desc(Buyer.created_at)).all()
    rows = [
        {
            "id": b.id,
            "company_name": b.company_name,
            "country": b.country,
            "city": b.city,
            "buyer_type": b.buyer_type,
            "contact_person": b.contact_person,
            "designation": b.designation,
            "email": b.email,
            "phone": b.phone,
            "website": b.website,
            "source": b.source,
            "product_interest": b.product_interest,
            "moq": b.moq,
            "price_discussed": b.price_discussed,
            "payment_terms": b.payment_terms,
            "status": b.status,
            "last_contact_date": b.last_contact_date,
            "next_follow_up_date": b.next_follow_up_date,
            "remarks": b.remarks,
            "created_at": b.created_at,
        }
        for b in buyers
    ]

    df = pd.DataFrame(rows)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="EU Buyers")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=EU_Turmeric_Buyers.xlsx"},
    )