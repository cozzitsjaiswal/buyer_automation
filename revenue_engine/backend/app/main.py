from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from . import models
from .api import router

app = FastAPI(title=settings.app_name, version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.on_event("startup")
def startup():
    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)

@app.get("/health")
def health(): return {"status":"ok","service":settings.app_name,"environment":settings.environment}

@app.get("/health/live")
def live(): return {"status":"alive"}

@app.get("/health/ready")
def ready():
    try:
        with engine.connect() as conn: conn.exec_driver_sql("SELECT 1")
        return {"status":"ready"}
    except Exception: return {"status":"not_ready"}

@app.get("/")
def root(): return {"service":settings.app_name,"docs":"/docs","version":"2.0.0"}
