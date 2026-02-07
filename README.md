# EU Buyer Automation System

Production-ready local web application for exporters to manage EU B2B buyers for spices/food ingredients.

## Architecture

- **Frontend:** React + Tailwind CSS SPA with sidebar navigation and business dashboard.
- **Backend:** FastAPI REST API with SQLAlchemy ORM.
- **Database:** SQLite (`eu_buyer_automation.db`) containing `buyers` table.
- **Automation:** URL import pipeline using `requests` + `BeautifulSoup` + regex extraction.
- **Export:** Pandas + OpenPyXL for one-click `.xlsx` export.

## Features

- Dashboard with totals, status cards, and latest 10 buyers.
- Add Buyer form mapped to complete schema with validation.
- Buyer list with search, status filter, inline status and remarks updates.
- Import URLs page for bulk website scraping and buyer auto-creation.
- One-click Excel export with filename `EU_Turmeric_Buyers.xlsx`.

## Project Structure

```text
backend/
  main.py
  database.py
  models.py
  scraper.py
  requirements.txt
frontend/
  src/
    components/
    pages/
    App.jsx
README.md
```

## Database Schema (`buyers`)

- id (auto)
- company_name
- country
- city
- buyer_type (Importer / Wholesaler / Processor)
- contact_person
- designation
- email
- phone
- website
- source (Google Maps / B2B / LinkedIn / Manual)
- product_interest (Turmeric / Dal / Multiple)
- moq
- price_discussed
- payment_terms
- status (New / Contacted / Sample Sent / Negotiation / Closed / Lost)
- last_contact_date
- next_follow_up_date
- remarks
- created_at

## Backend Setup (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://127.0.0.1:8000/docs`

## Frontend Setup (React + Tailwind)

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

## Core API Endpoints

- `GET /health`
- `POST /buyers`
- `GET /buyers?search=&status=`
- `GET /buyers/{id}`
- `PATCH /buyers/{id}`
- `DELETE /buyers/{id}`
- `GET /dashboard`
- `POST /import-urls`
- `GET /export`

## Usage Flow

1. Open Dashboard for KPIs.
2. Add buyers manually on **Add Buyer**.
3. Bulk import from websites on **Import URLs**.
4. Manage pipeline in **Buyer List** with status and remarks edits.
5. Export all records from **Export to Excel**.

